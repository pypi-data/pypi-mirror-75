from osgeo import ogr
import geoformat


def sql(path, sql_request):
    """
    GDAL/OGR dependence

    Execute sql request to indicate database

    :param path: path to database
    :param sql_request: resquest in string
    :return: ogr return of request
    """
    data_source = ogr.Open(path)
    return data_source.ExecuteSQL(sql_request)


def sql_select_to_geolayer(pg_adress, select_request, geolayer_name=None, field_name_filter=None, bbox_extent=True, bbox_filter=None,  feature_serialize=False, feature_limit=None, feature_offset=None):
    """
    Return a geolayer that is result to SQL request

    :param pg_adress: connexion database parameters
    :param select_request: sql request that we want to return
    :return: a geolayer that is result to given SQL request.
    """
    # drop view if exists
    sql_drop_view = """DROP VIEW IF EXISTS geoformat_temporary_view;"""
    sql(pg_adress, sql_drop_view)
    # create view request
    sql_create_view = """CREATE OR REPLACE VIEW geoformat_temporary_view AS (
    {select_request}
    );""".format(select_request=select_request)
    # execute request
    sql(pg_adress, sql_create_view)
    geolayer = geoformat.ogr_layer_to_geolayer(pg_adress,
                                               layer_id='geoformat_temporary_view',
                                               field_name_filter=field_name_filter,
                                               bbox_extent=bbox_extent,
                                               bbox_filter=bbox_filter,
                                               feature_serialize=feature_serialize,
                                               feature_limit=feature_limit,
                                               feature_offset=feature_offset
                                               )
    if geolayer_name:
        geolayer['metadata']['name'] = geolayer_name
    # drop the view
    sql_drop_view = """DROP VIEW geoformat_temporary_view;"""
    sql(pg_adress, sql_drop_view)

    return geolayer
