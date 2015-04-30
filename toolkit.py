#!/usr/bin/env python

__author__ = 'Eachan Johnson'

## Define classes
class LabnotiFile(object):

    def __init__(self, path, root, type):
        import time
        import os
        self.path = path
        self.filename = path.split('/')[-1]
        self.ext = self.filename.split('.')[-1]
        self.size = os.stat(self.path).st_size
        self.root = root
        self.type = self.get_type()
        self.epoch_date = self.get_date()
        self.date = time.strftime('%A, %B %d, %Y', time.localtime(self.epoch_date))
        self.tags = sorted(self.get_tags())
        self.html = self.htmlify()

    def get_date(self):
        import os.path
        import time
        date = os.path.getctime(filename=self.path)
        return date

    def get_tags(self):
        import os.path
        relative_pwd = ''
        pwd = self.path
        try:
            relative_pwd = pwd.split(self.root)[1].split(self.filename)[0]
        except IndexError:
            pass #print pwd, self.root, pwd.split(self.root)
        all_tags = [tag for tag in relative_pwd.split('/') + [self.type, self.ext] if tag != '']
        return all_tags

    def get_type(self):
        type_dict = {
            'png': 'image',
            'jpeg': 'image',
            'jpg': 'image',
            'pdf': 'PDF',
            'csv': 'CSV',
            'docx': 'Word DOCX',
            'doc': 'Word DOC',
            'xls': 'Excel XLSX',
            'xlsx': 'Excel XLSX',
            'R': 'code',
            'py': 'code',
            'md': 'Markdown'
        }
        try:
            t = type_dict[self.ext]
        except KeyError:
            t = 'unknown'
        return t

    def htmlify(self):
        #print 'HTMLifying ', self.filename
        if self.type == 'image':
            html = '<img src="../img/{}" />'.format(self.filename)
        elif self.type == 'code':
            html = '<pre><code>../code/{}</code><pre>'.format(open(self.path, 'rU').read())
        elif self.type == 'Markdown':
            import markdown
            converter = markdown.Converter()
            html = converter.convert(self.path)
        elif self.type == 'Excel XLSX':
            import xlrd
            import csv
            try:
                workbook = xlrd.open_workbook(self.path)
            except xlrd.biffh.XLRDError:
                html = ''
            else:
                sheet_names = workbook.sheet_names()
                for sheet_name in sheet_names:
                    sheet = workbook.sheet_by_name(sheet_name)
                    with open('.xltemp.csv', 'w') as f:
                        c = csv.writer(f, quoting=csv.QUOTE_ALL)
                        for rownum in xrange(sheet.nrows):
                            try:
                                c.writerow(sheet.row_values(rownum))
                            except UnicodeEncodeError:
                                c.writerow([''])
                html = self.csv_to_html(filename='.xltemp.csv')
        elif self.type == 'Word DOCX':
            from xml.etree.ElementTree import XML
            import zipfile
            WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
            PARA = WORD_NAMESPACE + 'p'
            TEXT = WORD_NAMESPACE + 't'
            docx = zipfile.ZipFile(self.path)
            xml_content = docx.read('word/document.xml')
            docx.close()
            tree = XML(xml_content)
            html = '<p>'
            paragraphs = []
            for paragraph in tree.getiterator(PARA):
                texts = [node.text
                         for node in paragraph.getiterator(TEXT)
                         if node.text]
                if texts:
                    paragraphs.append(''.join(texts))
            html += '</p><p>'.join(paragraphs)
            html += '</p>'
        elif self.type == 'CSV':
            html = self.csv_to_html(filename=self.path)
        else:
            html = ''
        return html

    def csv_to_html(self, filename):
        import csv
        if filename[0] != '.':
            html = '<table id={}>'.format(filename)
        else:
            html = '<table id={}>'.format(self.path)
        with open(filename, 'rU') as f:
            c = csv.reader(f)
            for row in c:
                html += '<tr><td>'
                html += '</td><td>'.join(row)
                html += '</td></tr>'
        html += '</table>'
        return html

    def __str__(self):
        s = 'Path:\t\t{}\n' \
            'Filename:\t{}\n' \
            'Size:\t\t{}\n' \
            'Root:\t\t{}\n' \
            'Type:\t\t{}\n' \
            'Date:\t\t{}\n' \
            'Tags:\t\t{}'.format(
            self.path,
            self.filename,
            self.size,
            self.root,
            self.type,
            self.date,
            ', '.join(self.tags)
        )
        return s


class Day(object):

    def __init__(self, file_list):
        self.epoch_date = file_list[0].epoch_date
        self.date = file_list[0].date
        #print 'Collating day', self.date, len(file_list)
        self.files = file_list
        self.filename = '{}_{}.html'.format(self.epoch_date, self.date)
        self.html = self.get_html()

    def get_html(self):
        print 'HTMLifying day ', self.date
        html = '<html><body><h1>{}</h1>'.format(self.date)
        for experiment in self.files:
            print experiment.path, experiment.size
            html += '<h3>' + ', '.join(experiment.tags) + '</h3>'
            try:
                html += '<section>' + experiment.html + '</section>'
            except UnicodeDecodeError:
                pass
        html += '</body></html>'
        return html

    def write(self, outdir):
        print 'Writing day', self.filename
        import os
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        with open('{}/{}'.format(outdir, self.filename), 'w') as f:
            try:
                f.write(self.html)
            except UnicodeEncodeError:
                pass
        return self.filename


class Notebook(object):

    def __init__(self, day_list):
        print 'Collating notebook'
        self.days = day_list
        self.filename = 'index.html'

    def __str__(self):
        print self.filename


def html_gen(notebook, outdir):

    import os

    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not os.path.exists(outdir+'/html'):
        os.makedirs(outdir+'/html')
    if not os.path.exists(outdir+'/img'):
        os.makedirs(outdir+'/img')
    if not os.path.exists(outdir+'/img'):
        os.makedirs(outdir+'/code')

    for day in notebook.days:
        day.write(outdir=outdir+'/html')
        for f in day.files:
            if f.type == 'image':
                try:
                    os.symlink(f.path, outdir+'/img/'+f.filename)
                except OSError:
                    pass
            elif f.type == 'code':
                os.symlink(f.path, outdir+'/code/'+f.filename)

    html = '<html><body><h1>Lab notebook</h1>'
    html += '<ul><li>'
    html += '</li><li>'.join(['<a href="html/{}">{}</a>'.format(day.filename, day.date) for day in notebook.days])
    html += '</li></ul></body></html>'

    filename = outdir + '/index.html'

    with open(filename, 'w') as f:
        f.write(html)
    return filename