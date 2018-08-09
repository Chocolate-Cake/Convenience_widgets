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

class entry:
	def __init__(self, arr):
		self.rep = []
		self.name = arr[1]
		self.webname = self.name.replace(" ", "_").replace("'", "_").lower()
		self.category = arr[2]
		self.description = arr[3]
		self.events = clean_items(arr[4])
		self.recruiting = arr[5].split(', ')
		self.rn = arr[6]
		self.re = arr[7]
		self.social_media = clean_social_media(arr[8])

		#About, Events, Recruitment, Contact, Tags
		format = [
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
			["<p>Custom tags go here</p>"]
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
		for item in self.list:
			#pages don't exist yet so placeholder is google
			format.append("<option value='https://www.google.com/'>" + item.name + "</option>")
			#format.append("<option value='" + item.name.replace(" ", "_").replace("'", "").lower() + "'>" + item.name + "</option>")
		format.append("</select>")
		format.append("<br><br>")
		format.append("<input id='" + self.webname + "_button' type='submit' value='Go'>")
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
		format.append("var temp = x.toLowerCase();")
		format.append("var next = '';")
		format.append("for (i = 0; i < temp.length; i++) {")
		problem_string = '"' + "'" + '"'
		format.append("if (temp.charAt(i) == ' ' || temp.charAt(i) == '/' || temp.charAt(i) == " + problem_string + ") {") 
		format.append("next = next + '_';")
		format.append("} else {")
		format.append("next = next + temp.charAt(i);")
		format.append("}}")
		format.append("next = next + '_desc'")
		format.append("var to_show = document.getElementById(next).textContent;")
		format.append("to_show = '<p>' + to_show + '</p>'")
		format.append("document.getElementById('" + self.webname + "_desc_box').innerHTML=to_show")
		format.append("}")
		format.append("</script>")

		return ("\n".join(format))

def put_in_table(items, max_width):
	index = 0
	format = []
	percent = 100.0/float(max_width);

	#format.append("<html><body>")
	format.append("<table>")
	while index<len(items):
		format.append("<tr>")
		for i in range(max_width): 
			if index < len(items):
				format.append("<td><center><br>")
				format.append("<h3>" + items[index].name + "</h3>")
				format.append(items[index].make_dropdown_html())
				format.append("</center></td>")
				index += 1
		format.append("</tr>")
	format.append("</table>")
	format.append("<style>")
	format.append("table { width:100%; }")
	format.append("input { font-size:1em; width: 40%; max-width: 100px; height: 40%; }")
	format.append("h3 { color:white; font-size:1.5em; }")
	format.append("td { background-color: #3E7ED5; width:" + str(percent) + "%; padding-top:0.3em; padding-bottom:0.3em; border: solid white 0.5em; }")
	format.append("select { font-size:1em; overflow: hidden; width: 80%; max-width: 400px; overflow: auto; } ")
	format.append(".desc_box { color: white; padding-left:1%; padding-right:1%; height: auto; max-height: 10em; overflow: auto; border-top: white solid 1px; border-bottom: white solid 1px;}")
	format.append("</style>")
	#format.append("</body></html>")
	f = open("dropdown.html", "w+")
	f.write("\n".join(format))
	f.close()
	#print ("\n".join(format))


with open('test.csv', 'rt', encoding="utf8") as csvfile:
		reader = csv.reader(csvfile)
		next(reader)
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
				f.write("\n\n\n")
			f.close()
		end_time = time.time()

		put_in_table(categorize, 2)

		'''
		print("Elapsed time: " + str((end_time - start_time)*1000) + " milliseconds")
		print("Unique entries: " + str(len(names)) + " out of " + str(counter) + " entries")
		print("Duplicates found: " + str(dups))
		print("Exceptions thrown: " + str(exceptions) + " out of " + str(counter * 9) + " items")
		'''
		print("DONE")





