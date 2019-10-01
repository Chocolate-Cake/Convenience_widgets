import csv, time, operator, os
import urllib.request
para_ovrd = "override_original"
empty_ovrd = "override_empty"
com_ovrd = "override_comma"
hyp_ovrd = "override_hyphen"
n_ovrd = "override_n"
semi_ovrd = "override_semi"
join_ovrd = "override_join"
per_ovrd = "override_period"

def handle_overrides(e):
	if len(e) > 0:
		first = e.split(" ")[0]
		if first.strip() == para_ovrd:
			return [e[len(para_ovrd)::]]
		elif first == empty_ovrd:
			return [""]
		elif first == com_ovrd:
			return e[len(com_ovrd)::].split(',')
		elif first == hyp_ovrd:
			return e[len(hyp_ovrd)::].split('-')
		elif first == n_ovrd:
			return e[len(n_ovrd)::].split('\n')
		elif first == semi_ovrd:
			return e[len(semi_ovrd)::].split(';')
		elif first == per_ovrd:
			return e[len(per_ovrd)::].split('.')
		elif first == join_ovrd:
			text = e[len(join_ovrd)::].split('\n')
			return ''.join(text)
	return None

def clean_items(e, when_one = "EXCEPTION THROWN: clean_items encountered unknown format"):
	special = handle_overrides(e)
	if special is not None:
		return special

	try_commas = e.split(',')
	try_nl = e.split('\n')
	try_sc = e.split(';')

	if len(try_nl) > 1 and len(try_commas) == 1 and len(try_sc) == 1:
		return [x.strip('-').strip() for x in try_nl]
	elif len(try_commas) > 1 and len(try_nl) == 1 and len(try_sc) == 1:
		return [x.strip() for x in try_commas]
	elif len(try_sc) > 1 and len(try_nl) == 1 and len(try_commas) == 1:
		return [x.strip() for x in try_sc]
	else:
		return [e]

def clean_social_media(sm):
	special = handle_overrides(sm)
	if special is not None:
		return special

	get_list = sm.split()
	to_return = []
	counter = 0
	for word in get_list:
		temp = word.strip(';').strip(',')
		if ".com" in word or ".org" in word or "http" in word or "www." in word:
			to_return.append("<a href='" + temp + "'>" + temp + "</a><br>")
			counter += 1
		else:
			to_return.append(word)
	
	if counter == 0:
		return sm
	else:
		return [' '.join(to_return)]

def capitalize_first(line):
	try:
		if len(line) == 0:
			return line

		if not line[0].isdigit():
			return line[0].upper() + line[1::]
		else:
			return line
	except _:
		return "EXCEPTION THROWN: capitalize_first encountered unknown format"

def list_displayer(l, capitalize = True):
	try:
		if l is not None and len(l) > 0 and not "Exception: func" in l[0]:
			result = '\t' + l[0]
			for x in range(1, len(l)):
				result += ("<br>" + '\t' + capitalize_first(l[x]))
			return result
	except _:
		pass

	suffix = ""
	if l is not None and "EXCEPTION THROWN: " in l[0]:
		suffix = " - inherited from " + l[0]
	
	return '\t' + "EXCEPTION THROWN: list_displayer failed" + suffix.lower()

def handle_join(thing, is_txt = False):
	if thing is None:
		return "None"
	if isinstance(thing, list):
		if is_txt:
			return '\n'.join(thing)
		else:
			return '<br>'.join(thing)
	else:
		return thing

#hard coded greek, stu gov, other
#all categories in front are auto because perfect match
cat_list = [
	"Academic/Pre-Professional",
	"Arts/Performance",
	"Community/Public Service",
	"Cultural/International",
	"Instructional/Competitive",
	"Media/Publication",
	"Peer Education/Support",
	"Political/Advocacy",
	"Religious/Spiritual",
	"Sports/Recreational",
	"Greek/Honor Society",
	"Student Government",
	"Other"]

def purge_non_alnum(my_str):
	changed = ""
	if my_str[0].isdigit():
		changed += "_"
	for c in my_str:
		if c == " ":
			changed += "_"
		elif c.isalnum():
			changed += c
	return changed

class entry:
	def __init__(self, arr):
		self.rep = []
		self.rep_show = []
		self.name = arr[1]
		self.webname = purge_non_alnum(self.name)
		self.urlname = self.name.strip().replace("/", "").replace(" ", "-").lower()
		self.category = arr[2]
		self.description = arr[3].replace("\n", "<br>")
		self.events = clean_items(arr[4])
		self.recruiting = arr[5].split(", ")
		self.recruiting_details = arr[6].replace("\n", "<br>")
		self.rn = arr[7]
		self.re = arr[8]
		self.social_media = clean_social_media(arr[9])


		#About, Events, Recruitment, Contact, Tags
		format = [
			["<div id='" + self.webname + "_div' style='display:none;'>"],
			["<font face = 'Arial' size = '3'>"],
			["<h1 style='background-color: #D6D6D6'>", self.name, "</h1>"],
			["</font>"],
			["<p>", handle_join(self.description), "</p>"],
			["<font face = 'Arial' size = '3'>"],
			["<h1 style='background-color: #D6D6D6'>Events</h1>"],
			["</font>"],
			["<p>", handle_join(self.events), "</p>"],
			["<font face = 'Arial' size = '3'>"],
			["<h1 style='background-color: #D6D6D6'>Recruitment</h1>"],
			["</font>"],
			["<p>", handle_join(self.recruiting), "</p>"],
			["<p><b> Additional details about recruiting: </b></p>"],
			["<p>" + self.recruiting_details + "</p>"],
			["<font face = 'Arial' size = '3'>"],
			["<h1 style='background-color: #D6D6D6'>Contact</h1>"],
			["</font>"],
			["<p><b>Name: </b>", handle_join(self.rn), "<br>"],
			["<b>Email address: </b>", self.re, "<br>"],
			["<b>Web: </b>", handle_join(self.social_media), "<br></p>"],
			["<div style='background-color: #D6D6D6; height: 2px;'></div>"],
			["</div>"]
		]
		concat = []
		#hidden_prefix = ["<div id='" + self.webname + "_div'>"]
		#show_prefix = ["<div id='" + self.webname + "_div'>"]
		
		for thing in format:
			concat.append(''.join(thing))
		self.rep.append(''.join(concat))
		#self.rep.append(''.join(hidden_prefix) + ''.join(concat))
		#self.rep_show.append(''.join(show_prefix) + ''.join(concat))

	def __repr__(self):
		return "".join(self.rep)

	def repr_show(self):
		return "".join(self.rep_show)

	def __str__(self):
		return self.__repr__()

class category_list:
	def __init__(self, name):
		self.name = name.replace("/", " / ")
		self.webname = name.replace(" ", "_").replace("/", "_").replace("-", "_").lower()
		self.list = []

	def append(self, item):
		self.list.append(item)

	def sort(self):
		self.list.sort(key=operator.attrgetter('name'))

	def make_dropdown_html(self):
		format = []
		for item in self.list:
			format.append("<div id='" + item.webname + "_desc' style='display:none;'>")
			format.append(item.description)
			format.append("</div>")

		format.append("<form id='" + self.webname + "'>")
		format.append("<select id='" + self.webname + "_select' onchange='" + self.webname + "_select_func()'>")
		format.append("<option value=''>Select</option>")
		for item in self.list:
			url_link = "https://sites.google.com/view/get-involved-at-penn/groups/" + item.category.replace("/", "").replace(" ", "-").lower() + "/" + item.urlname
			format.append("<option value='" + url_link + "'>" + item.name + "</option>")
			#format.append("<option value='" + item.name.replace(" ", "_").replace("'", "").lower() + "'>" + item.name + "</option>")
		format.append("</select>")
		#format.append("<br><br>")
		format.append("<input id='" + self.webname + "_button' type='submit' value='Learn more'>")
		format.append("</form>")

		format.append("<div id='" + self.webname + "_desc_box' class='desc_box' style='display:auto;'>")
		format.append("</div>")

		format.append("<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js'></script>")
		#submit button function
		format.append("<script>")
		format.append("$('#" + self.webname + "').on('submit', function (e) {")
		format.append("e.preventDefault();")
		format.append("var $form = $(this),")
		format.append("$select = $form.find('select'),")
		format.append("links = $select.val();")
		format.append("if(links.length>0) {")
		format.append("window.open(links, '_blank');}});")
		format.append("</script>")
		#select on change
		format.append("<script>")
		format.append("function " + self.webname + "_select_func() {")
		format.append("var x = $('#" + self.webname + "_select>option:selected').text();")
		format.append("if (x != 'Select') {")
		format.append("var temp = x.toLowerCase();")
		format.append("var next = '';")
		format.append("for (i = 0; i < temp.length; i++) {")
		problem_string = '"' + "'" + '"'
		format.append("if (temp.charAt(i) == ' ' || temp.charAt(i) == '/' || temp.charAt(i) == " + problem_string + ") {") 
		format.append("next = next + '_';")
		format.append("} else {")
		format.append("next = next + temp.charAt(i);")
		format.append("}}")
		format.append("next = next + '_desc';")
		format.append("var to_show = document.getElementById(next).textContent;")
		format.append("to_show = '<p><b>Description</b><br>' + to_show + '</p>'")
		format.append("document.getElementById('" + self.webname + "_desc_box').innerHTML=to_show")
		format.append("}")
		format.append("}")
		format.append("</script>")

		return ("\n".join(format))

def put_in_divs(items, target):
	index = 0
	format = []

	#format.append("<html><body>")
	format.append("<div id='outer_div'><center>")
	while index<len(items):
		format.append("<div class='floater_div'>")
		#format.append("<br>")
		format.append("<h3>" + items[index].name + "</h3>")
		format.append(items[index].make_dropdown_html())
		format.append("")
		format.append("</div>")
		index += 1
	format.append("</center></div>")

	format.append("<style>")
	format.append("input { font-size:1em; max-width: 50%; max-width: 100px; max-height: 50%; }")
	format.append("h3 { color:white; font-size:1.4em; height:vh*10%; }")
	format.append("select { font-size:1em; overflow: hidden; width: 80%; max-width: 400px; overflow: auto; } ")
	format.append(".desc_box { background-color: none; color: white; padding-left:5%; padding-right:5%; height: auto; height: 10em; overflow: auto; border-top: white solid 1px; border-bottom: white solid 1px;}")
	format.append("#outer_div {max-width: vw; max-height: vh; overflow: auto;}")
	format.append(".floater_div { text-align:center; padding: 1%; margin: 0px; border: solid white 0.1em; background-color: #3E7ED5; float: none; display:inline-block; width: 18em; height:auto; max-height: 20em;}")
	format.append("</style>")
	f = open(target, "w+")
	f.write("\n".join(format))
	f.close()

def categories_from_reader(reader, skips):
	for _ in range(skips):
		next(reader)

	categorize = []
	for x in range(len(cat_list)):
		categorize.append(category_list(cat_list[x]))
	names = set()
	dups = []
	counter = 0
	acc = ""
	for row in reader:
		counter += 1
		g = entry(row)
		if g.name.lower() not in names:
			names.add(g.name.lower())
			if g.category in cat_list:
				categorize[cat_list.index(g.category)].append(g)
			elif "greek" in g.name.lower() or "greek" in g.category.lower():
				categorize[len(categorize)-3].append(g)
			elif "govern" in g.name.lower() or "govern" in g.category.lower():
				categorize[len(categorize)-2].append(g)
			else:
				categorize[len(categorize)-1].append(g)
		else:
			dups.append(g.name)
	return categorize, str(len(names)), dups, counter

def make_category_pages(my_csv, skips, make_txt_files = False):
	with open(my_csv, 'rt', encoding="utf8") as csvfile:
		reader = csv.reader(csvfile)
		start_time = time.time()
		exceptions = 0
		categorize, uniques, dups, counter = categories_from_reader(reader, skips)
		if make_txt_files:
			count = 0
			for i in categorize:
				i.sort()
				f = open(cat_list[count].lower().replace("/", "_") + ".txt", "w+")
				count += 1
				for j in i.list:
					f.write(j.name)
					f.write("\n")
					f.write(j.__repr__())
					exceptions += j.__repr__().count("EXCEPTION THROWN")
					f.write("\n\n\n\n\n")
				f.close()
		end_time = time.time()
		f = open("logs.txt", "w+")
		f.write("Elapsed time: " + str((end_time - start_time)*1000) + " milliseconds\n\n")
		f.write("Unique entries: " + uniques + " out of " + str(counter) + " entries\n\n")
		f.write("Duplicates found: \n" + handle_join(dups, is_txt = True) + '\n\n')
		f.write("Exceptions thrown: " + str(exceptions) + " out of " + str(counter * 9) + " items\n\n")
		f.close()
		return categorize

def make_category_names_list(categorize, target):
	f = open(target, "w+")
	for item in categorize:
		f.write(item.name + "\n")
		for i in item.list:
			f.write(i.name + "\n")
		f.write("\n\n\n")

def make_separate_category_dropdowns(categorize):
	index = 0
	for category in categorize:
		category.list.sort(key=lambda x: x.name)
		format = []
		counter = 1
		format.append("<html><head><style>")
		format.append("button { font-size: 100%; width:70%; height:auto; margin: 10px; padding: 10px;}")
		format.append("body { text-align: center;}")
		format.append("p { font-size: 20px;}")
		format.append("</style></head><body>")
		for item in category.list:
			format.append("<div style: 'text-align:center;'>")
			format.append("<button id='" + item.webname + "_div_button' type='button' onclick='" + item.webname + "_div_func()'>")
			format.append(item.name)
			format.append("</button>")
			format.append("<div>")
			format.append(item.__repr__())
			format.append("<script>")
			format.append("function " + item.webname + "_div_func() {")
			format.append("var x = document.getElementById('" + item.webname + "_div');")
			format.append("var b = document.getElementById('" + item.webname + "_div_button');")
			format.append("if (x.style.display == 'none') {")
			format.append("x.style.display='block'; b.style.backgroundColor='#569BF9';} else {")
			format.append("x.style.display='none'; b.style.backgroundColor='white';")
			format.append("}}")
			format.append("</script>")
			counter += 1
		format.append("</body></html>")
		f = open(cat_list[index].lower().replace("/", "_") + ".html", "w+")
		f.write('\n'.join(format))
		f.close()
		index += 1
		

def make_single_page_drop_downs(categorize, target):
	format = []
	format.append("<html><head><style>")
	format.append("button { font-size: 100%; width:50%; height:10%; max-height:15%; margin: 10px;}")
	format.append("body { text-align: center;}")
	format.append("p { font-size: 20px;}")
	format.append("</style></head><body>")
	for category in categorize:
		counter = 1
		format.append("<h1>-------------" + category.name + "-------------</h1>")
		for item in category.list:
			format.append("<div style: 'text-align:center;'>")
			format.append("<button id='" + item.webname + "_div_button' type='button' onclick='" + item.webname + "_div_func()'>")
			format.append("(" + str(counter) + ".)  " + item.name)
			format.append("</button>")
			format.append("<div>")
			format.append(item.__repr__())
			format.append("<script>")
			format.append("function " + item.webname + "_div_func() {")
			format.append("var x = document.getElementById('" + item.webname + "_div');")
			format.append("var b = document.getElementById('" + item.webname + "_div_button');")
			format.append("if (x.style.display == 'none') {")
			format.append("x.style.display='block'; b.style.backgroundColor='#569BF9';} else {")
			format.append("x.style.display='none'; b.style.backgroundColor='white';")
			format.append("}}")
			format.append("</script>")
			counter += 1
	format.append("</body></html>")
	f = open(target, "w+")
	f.write('\n'.join(format))

def make_randomize_all(categorize, target):
	format = []
	total = 0
	format.append("<html><head><style>")
	format.append("button { font-size: 100%; width:50%; height:10%; max-height:15%; margin: 10px;}")
	format.append("body { text-align: center;}")
	format.append("p { font-size: 20px; text-align: left;}</style>")
	format.append("<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js'></script>")
	format.append("</head><body>")
	for category in categorize:
		for item in category.list:
			format.append(item.__repr__())
			total += 1
	format.append("<center>")
	format.append("<button type='button' onclick='get_random()'> Give me a random group </button>")
	format.append("</center>")
	format.append("<div id='randomized_div'></div>")
	format.append("<script>")
	format.append("function get_random() {")
	format.append("var get_divs = $(" + '"' + "div[id*='_div']" + '"' + ");")
	format.append("var rand_num = Math.floor(Math.random() * " + str(total) + ");")
	format.append("var to_show = get_divs[rand_num].innerHTML;")
	format.append("document.getElementById('randomized_div').innerHTML=to_show;")
	format.append("}")
	format.append("</script>")
	format.append("</body></html>")
	f = open(target, "w+")
	f.write('\n'.join(format))

def tables():
	with open("numbers.csv", 'rt', encoding="utf8") as csvfile:
			reader = csv.reader(csvfile)
			format = []
			f = open("num_tables.html", "w+")
			format.append("<html><head>")
			format.append("</head><table><tbody>")
			for row in reader:
				format.append("<tr>")
				format.append("<td>")
				format.append(row[0])
				format.append("</td>")
				format.append("<td>")
				format.append(row[1])
				format.append("</td>")
				format.append("<td>")
				format.append(row[2])
				format.append("</td>")
				format.append("</tr>")
			format.append("</tbody></table>")
			format.append("<style>")
			format.append("td {width = 100px;}")
			format.append("</style>")
			format.append("</html>")
			

	f.write(''.join(format))

#cat = make_categories_from_url("https://docs.google.com/spreadsheets/d/1_YNkvj7wdj3kkmogLv2LO0RDTaRNgQJAA4om9tRuPoc/edit#gid=0", 2)
#put_in_divs(cat, "web_stuff.html")
#make_category_names_list(cat, "names_list.txt")
#make_single_page_drop_downs(cat, "web_stuff.html")

'''
#get category object & make txt files
cat = make_category_pages("responses_all.csv", 0, True)
#make page with randomized results
make_randomize_all(cat, "web_stuff.html")
#make pages with buttons that drop down, by category
make_separate_category_dropdowns(cat)
'''

tables()



