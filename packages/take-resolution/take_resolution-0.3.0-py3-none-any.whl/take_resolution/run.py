__author__ = 'Gabriel Salgado'
__version__ = '0.3.0'

import typing as tp
import pyspark as ps
from take_resolution.utils import load_params
from take_resolution.bot_flow.bot_flow import build_dataframe
from take_resolution.bot_flow.bot_flow import select_bot
from take_resolution.bot_flow.bot_flow import select_flow
from take_resolution.bot_flow.bot_flow import query


CONTEXT = ps.SQLContext


def run(sql_context: CONTEXT, bot_identity: str) -> tp.Dict[str, tp.Any]:
	"""Run TakeResolution."""
	params = load_params()
	
	bot_flow_database = params['bot_flow_database']
	bot_flow_table = params['bot_flow_table']
	sp_df = build_dataframe(sql_context, bot_flow_database, bot_flow_table)
	
	bot_column = params['bot_column']
	application_column = params['application_column']
	application_value = params['application_value']
	sp_df_selected = select_bot(sp_df, bot_column, bot_identity, application_column, application_value)
	
	flow_column = params['flow_column']
	sp_df_flow = select_flow(sp_df_selected, flow_column)
	
	df_flow_raw = query(sp_df_flow)
	
	return {
		'params': params,
		'result': df_flow_raw
	}
