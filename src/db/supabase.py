import os

import supabase
from config import SUPABASE_URL, SUPABASE_SECRET_KEY


sb = supabase.create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)


def check_rate_limit(ip):
	result = sb.rpc("check_request", {"p_identifier": ip}).execute()
	data = result.data[0]
	if data['is_allowed'] == True:
		return True
	else:
		return f'{data["blocked_until_time"]}'

def insert_check_logs(ip, text):
	response = sb.table("request_logs").insert({'identifier': ip, 'text': text}).execute()
	print(f'supabase inserted {response}')
	return response