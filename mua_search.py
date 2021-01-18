import face_detection as face
import skin_range_creation as tone

from googleapiclient.discovery import build

API_KEY = 'not for you'
YT_IMG_URL_FRONT = "https://i.ytimg.com/vi/"
YT_IMG_URL_BACK = "/hqdefault.jpg"


def get_yt_search():
	"""
		Returns a JSON
	"""
	youtube = build('youtube', 'v3', developerKey=API_KEY)

	# grab search JSON
	request = youtube.search().list(
		part="snippet",		# determines that you get thumbnails
		maxResults=10,		# make 25 later
		#q=create_search_terms() + " makeup tutorial"
		q="makeup tan tone tutorial"
	)
	response = request.execute()

	return response

def create_search_result_list(thumb_list, vid_id_list):
	search_results = {}
	i = 0
	while i < len(thumb_list):
		search_results[vid_id_list[i]] = thumb_list[i]
		i += 1
	return search_results

def get_thumbnails(yt_search):
	thumbnail_url_list = []
	for result in yt_search["items"]:
		snippet = result.get("snippet")
		thumbnails = snippet.get("thumbnails")
		hq_thumb = thumbnails.get("high")
		thumb_url = hq_thumb.get("url")
		thumbnail_url_list.append(thumb_url)
	return thumbnail_url_list

def get_vid_ids(yt_search):
	video_id_list = []
	for result in yt_search["items"]:
		id_info = result.get("id")
		vid_id = id_info.get("videoId")
		video_id_list.append(vid_id)
	return video_id_list

def create_search_terms(tone_terms, addl_terms):
	query = tone_terms + " " + addl_terms
	return query

def main():
	yt_search = get_yt_search()
	print(create_search_result_list(get_thumbnails(yt_search), get_vid_ids(yt_search)))


if __name__ == '__main__':
	main()