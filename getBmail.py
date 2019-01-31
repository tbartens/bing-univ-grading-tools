#! /usr/bin/python3

# Extract bmail id from myCourses USER view.  First, browse myCourses Users, select show all, right click to view source and save html
# Feed the result into this script, which will write a CSV that contains bnumber, name, and bmail


from html.parser import HTMLParser
import fileinput

class MyHTMLParser(HTMLParser):
	def __init__(self) :
		super().__init__()
		self.inRow=False
		self.rowId='?'
		self.bnumPending=False
		self.bnumPendingSave=False
		self.bnum='?'
		self.cnamPending=False
		self.cvalPending=False
		self.fnamPending=False
		self.fnam='?'		
		self.lnamPending=False
		self.lnam='?'
		self.emailPending=False
		self.email='?'
		self.rolePending=False
		self.role='?'
		print('"B-Number","Name","bmail"')
		
	def handle_starttag(self, tag, attrs):
		# print("Encountered a start tag:", tag)
		if (self.inRow) :
			# <span class="profileCardAvatarThumb"> 
			if (tag == 'a') :
				# Turn off bnumPending inside a tags
				self.bnumPendingSave = self.bnumPending
				self.bnumPending=False
			if (tag == 'span') :
				for attr in attrs :
					if (attr[0] == 'class') :
						# print("in row, span class is: ",attr[1])
						if (attr[1] == 'profileCardAvatarThumb') :
							self.bnumPending=True
						if (attr[1] == 'mobile-table-label') :
							self.cnamPending=True
						if (attr[1] == 'table-data-cell-value') :
							self.cvalPending=True
		if (tag == 'tr') :
			for attr in attrs :
				# print("attr: ",attr);
				if (attr[0] == 'id') :
					if (attr[1].startswith('listContainer_row:')) :
						# print("table row, id:", attr[1])
						self.rowId=attr[1];
						self.inRow=True	

	def handle_endtag(self, tag):
		# print("Encountered an end tag :", tag)
		if (self.inRow and tag=='tr') :
			if (self.role=='Student') :
				print('"'+self.bnum+'","'+self.fnam+' '+self.lnam+'","'+self.email+'"')
				# print("Bnum: ",self.bnum, "Name:", self.fnam, self.lnam, "email: ", self.email)
			self.rowId='?'
			self.inrow=False
			self.bnum='?'
			self.fnam='?'
			self.lnam='?'
			self.email='?'
			self.role='?'
		if (tag == 'a') :
			self.bnumPending=self.bnumPendingSave

	def handle_data(self, data):
		# print("Encountered some data  :", data)
		if (data.strip()== "") : return
		if (self.bnumPending) :
			self.bnum=data.strip()
			self.bnumPending=False
		if (self.cnamPending) :
			if (data.strip() == "First Name:") :
				self.fnamPending=True
			elif (data.strip() == 'Last Name:') :
				self.lnamPending=True
			elif (data.strip() == 'Email:') :
				self.emailPending=True
			elif (data.strip() == 'Role:') :
				self.rolePending=True
			# else : print("  Col name: ",data)
			self.cnamPending=False
		if (self.cvalPending) :
			# print("  Col Val: ",data)
			if (self.fnamPending) :
				self.fnam=data.strip()
				self.fnamPending=False
			if (self.lnamPending) :
				self.lnam=data.strip()
				self.lnamPending=False
			if (self.emailPending) :
				self.email=data.strip()
				self.emailPending=False
			if (self.rolePending) :
				self.role=data.strip()
				self.rolePending=False
			self.cvalPending=False

parser = MyHTMLParser()
for line in fileinput.input():
	parser.feed(line)