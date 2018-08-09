import csv, time, operator, os

def clean_items(e, when_one = "EXCEPTION THROWN: clean_items encountered unknown format"):
	try:
		try_commas = e.split(',')
		try_nl = e.split('\n')
		try_sc = e.split(';')

		if len(try_nl) > 1 and len(try_commas) == 1 and len(try_sc) == 1:
			return [x.strip('-').strip() for x in try_nl]
		elif len(try_commas) > 1 and len(try_nl) == 1 and len(try_sc) == 1:
			return [x.strip() for x in try_commas]
		elif len(try_sc) > 1 and len(try_nl) == 1 and len(try_commas) == 1:
			return [x.strip() for x in try_sc]
		elif len(try_commas) == 1 and len(try_nl) == 1 and len(try_sc) == 1:
			return [when_one]
	except _:
		return ["EXCEPTION THROWN: clean_items encountered unknown format"]

def clean_social_media(sm):
	try:
		if len(sm) == 1 and sm[0].lower == "none":
			return ["None"]
		elif len(sm) > 0:
			return clean_items(sm, when_one=sm)
	except _:
		pass
	return ["EXCEPTION THROWN: clean_social_media encountered unknown format"]

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

def handle_join(thing):
	if thing is None:
		return "None"
	if isinstance(thing, list):
		return '<br>'.join(thing)
	else:
		return thing

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
	"Student Government",
	"Other"
	]

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
		self.name = arr[1]
		self.webname = purge_non_alnum(self.name)
		self.urlname = self.name.strip().replace("/", "").replace(" ", "-").lower()
		self.category = arr[2]
		self.description = arr[3].replace("\n", "<br>")
		self.events = clean_items(arr[4])
		self.recruiting = arr[5].split(', ')
		self.rn = arr[6]
		self.re = arr[7]
		self.social_media = clean_social_media(arr[8])

		#About, Events, Recruitment, Contact, Tags
		format = [
			["<div id='" + self.webname + "_div' style='display:none;'>"],
			["<font face = 'Verdana' size = '3'>"],
			["<h1 style='background-color: #D6D6D6'>About</h1>"],
			["</font>"],
			["<p>", handle_join(self.description), "</p>"],
			["<font face = 'Verdana' size = '3'>"],
			["<h1 style='background-color: #D6D6D6'>Events</h1>"],
			["</font>"],
			["<p>", handle_join(self.events), "</p>"],
			["<font face = 'Verdana' size = '3'>"],
			["<h1 style='background-color: #D6D6D6'>Recruitment</h1>"],
			["</font>"],
			["<p>", handle_join(self.recruiting), "</p>"],
			["<font face = 'Verdana' size = '3'>"],
			["<h1 style='background-color: #D6D6D6'>Contact</h1>"],
			["</font>"],
			["<b>Name: </b>", handle_join(self.rn), "<br>"],
			["<b>Email address: </b>", self.re, "<br>"],
			["<b>Organization website: </b>", handle_join(self.social_media), "<br>"],
			["<font face = 'Verdana' size = '3'>"],
			["<h1 style='background-color: #D6D6D6'>Tags</h1>"],
			["</font>"],
			["<p>Custom tags go here</p>"],
			["</div><br>"]
		]
		concat = []
		for thing in format:
			concat.append(''.join(thing))
		self.rep.append(''.join(concat))

	def __repr__(self):
		return "".join(self.rep)

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

def make_category_files(my_csv, skips):
	with open(my_csv, 'rt', encoding="utf8") as csvfile:
			reader = csv.reader(csvfile)
			for _ in range(skips):
				next(reader)

			categorize = []
			for x in range(12):
				categorize.append(category_list(cat_list[x]))
			
			names = set()
			dups = []
			exceptions = 0
			counter = 0
			start_time = time.time()

			for row in reader:
				counter += 1
				g = entry(row)
				if g.name.lower() not in names:
					names.add(g.name.lower())
					if g.category in cat_list:
						categorize[cat_list.index(g.category)].append(g)
					elif "govern" in g.name.lower():
						categorize[len(categorize)-2].append(g)
					else:
						categorize[len(categorize)-1].append(g)
				else:
					dups.append(g.name)

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
			f.write("Elapsed time: " + str((end_time - start_time)*1000) + " milliseconds\n")
			f.write("Unique entries: " + str(len(names)) + " out of " + str(counter) + " entries\n")
			f.write("Duplicates found: " + str(dups) + '\n')
			f.write("Exceptions thrown: " + str(exceptions) + " out of " + str(counter * 9) + " items\n")
			return categorize

def make_category_names_list(categorize, target):
	f = open(target, "w+")
	for item in categorize:
		f.write(item.name + "\n")
		for i in item.list:
			f.write(i.name + "\n")
		f.write("\n\n\n")

def make_single_page_show_hide(categorize, target):
	format = []
	format.append("<html><head><style>")
	format.append("button { font-size: 100%; width:50%; height:10%; height: auto; max-height:150px; margin: 5px;}")
	format.append("body { text-align: center;}")
	format.append("p { font-size: 20px;}")
	format.append("</style></head><body>")
	for category in categorize:
		for item in category.list:
			format.append("<button id='" + item.webname + "_div_button' type='button' onclick='" + item.webname + "_div_func()'>")
			format.append("'" + item.name + "'")
			format.append("</button>")
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
	format.append("</body></html>")
	f = open(target, "w+")
	f.write('\n'.join(format))

cat = make_category_files("test.csv", 2)
#put_in_divs(cat, "web_stuff.html")
#make_category_names_list(cat, "names_list.txt")
make_single_page_show_hide(cat, "web_stuff.html")








