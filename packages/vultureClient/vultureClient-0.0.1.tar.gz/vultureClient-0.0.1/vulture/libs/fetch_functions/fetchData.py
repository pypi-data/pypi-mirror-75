import pandas as pd
# from deltametadata.deltametadata.readers.base_reader import BaseReader
# DATA_SOURCES = BaseReader.get_DATA_SOURCES()

DATA_SOURCES = ['mobius_ProductService', 'fpds', 'govshop', 'mobius_AboutUs', 'mobius_Awards',
                'mobius_Certifications', 'mobius_Contracts', 'mobius_linkedin', 'mobius_SBA',
                'pastexperience', 'tatras_scrapper']
FIELD_CHECKLIST = ['description', 'clean_description', 'lemma_clean_description','stem_clean_description','noun_phrases']


def combining_data(combine_descs,data_cursor,sources,fields):
    for rec in data_cursor:
        comb_desc = traversing_record(rec, sources, fields)
        if combine_descs == 'combined_desc':
            if len(fields)==1:
                col_name = fields[0]
            else:
                col_name = combine_descs
            comb_desc = {col_name : ' '.join(comb_desc.values())}
        elif combine_descs == 'source_level':
            pass
        comb_desc['supplier_id'] = rec['supplier_id']
        yield comb_desc

def output_batch(data_cursor,batch_size):
    batch = []
    for sr, rec in enumerate(data_cursor, 1):
        batch.append(rec)
        if sr % batch_size == 0:
            yield batch
            batch = []
    if len(batch) > 0:
        yield batch

def output_format(output,data_cursor,batch_size):
    if output == 'list':
        return list(data_cursor)
    elif output == 'cursor':
        return data_cursor
    elif output == 'batch':
        return output_batch(data_cursor,batch_size)
    else:
        raise Exception('Invalid output format.!! ')



def traversing_record(rec,sources,fields):
    ### Combine . paake krna yaa bina fullstop de ???
    src = set(rec.keys()).intersection(sources)
    res = dict()
    if len(src) > 0:
        for s in src:
            desc = traversing_record(rec[s],sources,fields)
            if desc:
                res[s] = desc

    flds = set(rec.keys()).intersection(fields)
    if len(flds) > 0:
        for fld in flds:
            if type(rec[fld]) == str:
                res_fld = rec[fld]
            elif type(rec[fld]) == dict:
                res_fld = traversing_record(rec[fld],sources,fields)
            elif type(rec[fld]) == list:
                res_lst = [x if type(x)==str else traversing_record(x,sources,fields) for x in rec[fld]]
                res_fld = '. '.join(res_lst)

        if fld in FIELD_CHECKLIST:
            return res_fld
        else:
            res[fld] = res_fld
    return res

class FetchVultureData:
    def __init__(self,vulture_conn):
        '''
        Class to Fetch data from VultureDB
        Args:
            vulture_conn: Mongo Collection object of vulture collection in Vulture DB
        '''
        self.vulture_conn = vulture_conn

    def get_suppliers_by_id(self,ids,sources=None,fields='clean_description',custom_selection=None,combine_descs = None, output='list',batch_size=1,**kwargs):
        """
        Get supplier data from the Vulture DB for the requested supplier ID(s)
        Args:
            ids: List of Supplier ID(s) for which we want to fetch data (Interger Type of IDs)
            sources: List of Data Source(s) which we want to fetch. If nothing is mentioned, it will fetch data from all sources.
            fields: Name/List of the data field(s) want to fetch. Default-> 'clean_description: which is the base clean version
            custom_selection: List of custom selections i.e. if we want to take clean description from one source and
            lemma description from other source, Ex: ['govshop.clean_description','pastexperience.lemma_clean_description']
            combine_descs: One of the following options to choose from ['combined_desc', 'source_level', None], Default value: None
            'combined_desc' will combine all the descriptions from all sources into a single description. 'source_level' will combine the descripitons
            for each source. None will return the data as is it is present in db
            output: ['list', 'cursor', 'batch'] Default: 'list'. It tell which form of output to return.
            'list' will return list of objects(dicts) of the data. 'cursor' will return the mongo cursor on the you can iterate.
            'batch' will also return an iterator but each iteration will contain a batch of the data.
            batch_size: Size of the batch if you want the output in batches. Default: 1
            **kwargs:

        Returns:
            Supplier id and data field in the format which is requested in the function call.
        """
        if type(ids) == int or type(ids)==str or type(ids)==float: ## single id
            ids = [int(float(ids))]
        if type(ids) != list:
            ids = list(ids)

        query = {'supplier_id':{'$in':ids}}
        projections = {'_id': 0}
        if fields:
            projections['supplier_id'] = 1
            if type(fields)==str:
                fields = [fields]
            if sources:
                pass
            else:
                sources = DATA_SOURCES
            for field in fields:
                for src in sources:
                    if field not in FIELD_CHECKLIST:
                        projections[field] = 1
                    else:
                        projections[src+'.'+field] = 1
        elif sources:
            projections['supplier_id'] = 1
            if type(sources) == str:  ##single source
                sources = [sources]
            for src in sources:
                projections[src] = 1

        if custom_selection:
            projections['supplier_id'] = 1
            for sel in custom_selection:
                projections[sel] = 1
                cus_srcs = set(sel.split('.')).intersection(DATA_SOURCES)
                sources.extend(list(cus_srcs))
                cus_flds = set(sel.split('.')).intersection((FIELD_CHECKLIST))
                fields.extend(list(cus_flds))
        else:
            if sources is None:
                sources = DATA_SOURCES

        print(query,projections)

        data_cursor = self.vulture_conn.find(query,projections)
        if combine_descs:
            comb_desc_iter = combining_data(combine_descs,data_cursor,sources,fields)
            res = output_format(output,comb_desc_iter,batch_size)
        else:
            res = output_format(output,data_cursor,batch_size)

        return res

    def get_ancestor_codes_of_suppliers(self,suppliers,catalog,conn):
        '''
        Get the Ancestor Codes of the Suppliers
        Args:
            suppliers: List of Supplier ID(s) for which we want to fetch data (Interger Type of IDs)
            catalog: Name of the catalog to choose from , 'naics' or any other etc.
            conn: psf psql connection object

        Returns: list of all the ancestors/top level codes to which the suppliers belong

        '''
        if type(suppliers) == str or type(suppliers) == int:
            suppliers = [suppliers]
        suppliers = [str(x) for x in suppliers]
        suppliers = ", ".join(suppliers)
        query = f""" WITH RECURSIVE nodes(id, parent_id,code) AS (
                    SELECT s1.id, s1.parent_id, s1.code
                    FROM suppliers_offering s1 WHERE  s1.catalog='{catalog}' and
                     s1.id in (Select offering_id from suppliers_company_offerings sco where sco.company_id in ({suppliers}))
                    UNION ALL
                    SELECT s2.id, s2.parent_id, s2.code
                    FROM suppliers_offering s2, nodes where nodes.parent_id = s2.id and catalog = '{catalog}'
                    )
                    SELECT distinct code FROM nodes where parent_id is null
                    ;"""
        df = pd.read_sql_query(query, con=conn)
        codes = df['code'].tolist()
        return codes

    def get_suppliers_by_commodity_codes(self,codes,catalog,conn,**kwargs):
        '''
        Get the supplier data which belongs to the given code(s)
        Args:
            codes: List of Code(s) for which you want the supplier IDs
            catalog: Name of the catalog in which you want to search
            conn: psf psql connection object
            **kwargs: all the arguments of get_suppliers_by_id function

        Returns:
            Supplier id and data field in the format which is requested in the function call.
        '''
        if type(codes) == str or type(codes) == int:
            codes = [codes]

        codes = "', '".join(codes)
        query = f"""select distinct sco.company_id 
        FROM
        (select id,code from suppliers_offering where catalog='{catalog}' and code in ('{codes}')) so
        INNER JOIN
        suppliers_company_offerings sco
        ON
        so.id=sco.offering_id
        """
        supplier_ids = pd.read_sql_query(query, con=conn)['company_id'].to_list()

        return self.get_suppliers_by_id(supplier_ids,**kwargs)

