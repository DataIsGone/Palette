import face_detection

# rgb, not bgr
skin_ranges = [
	# [(min), (max)]
	[(45, 34, 30), (105, 80, 70)],			# range 0
	[(105, 80, 70), (180, 138, 120)],		# range 1
	[(180, 138, 120), (255, 195, 170)],		# range 2
	[(255, 195, 170), (255, 229, 200)]		# range 3
]

range_terms = dict([
	(0, "dark deep tone"),
	(1, "dark tone"),
	(2, "tan tone"),
	(3, "fair tone")
	])


def get_skin_range_int(rgb):	# argument: brg --> rgb
	red, green, blue = (0, 1, 2)
	# user_r = rgb[red]
	# user_g = rgb[green]
	# user_b = rgb[blue]
	user_r, user_g, user_b = rgb
	user_skin_range = -999

	range_index = 0
	for curr_range in skin_ranges:
		curr_min = curr_range[0]
		curr_max = curr_range[1]
		if ((check_rgb(user_r, curr_min[red], curr_max[red]))
			and (check_rgb(user_g, curr_min[green], curr_max[green])) 
			and (check_rgb(user_b, curr_min[blue], curr_max[blue]))):

			user_skin_range = range_index
			break;

		range_index += 1

	if user_skin_range == -999:
		print("Error found -- could not match skintone")

	return user_skin_range


def get_tone_terms(skin_range_int):
	tone_terms = ""
	if skin_range_int in range_terms:
		tone_terms = range_terms[skin_range_int]
		return tone_terms
	else:
		print("Error found -- could not match skintone")

def get_yt_skin_avg(yt):
	get_avg_color(yt)


def get_matched_results(user_tone, thumbnail_list):	# uses bgr format
	blue, green, red = (0, 1, 2)
	matched_results = []
	for thumb in thumbnail_list:
		# arbitrary values, need to improve later
		if ((user_tone[blue] - 10 <= thumb[blue] <= user_tone[blue] + 10) 
			and (user_tone[green] - 10 <= thumb[green] <= user_tone[green] + 10) 
			and (user_tone[blue] - 10 <= thumb[blue] <= user_tone[blue] + 10)):

			matched_results.append(thumb)

	return matched_results



def check_rgb(user_rgb, curr_rgb_min, curr_rgb_max):
	if (user_rgb <= curr_rgb_max) and (user_rgb >= curr_rgb_min):
		return True
	return False


def main():
	print(get_tone_terms(get_skin_range_int((225, 172, 150))))