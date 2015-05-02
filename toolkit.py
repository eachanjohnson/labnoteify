#!/usr/bin/env python

from __future__ import division

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
        date = os.path.getctime(filename=self.path)
        return date

    def get_tags(self):
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
            'pptx': 'Powerpoint PPTX',
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
        #print 'HTMLifying ', self.path
        html = ''
        if self.type == 'image':
            import os.path
            if '.noteify' in self.filename and '.png' in self.filename:
                html = ''
            else:
                html = '<img src="../img/{}" height="500" />'.format(self.filename)
        elif self.type == 'code':
            html = '<pre style="background-color:rgba(0, 0, 255, 0.2);"><code>{}</code></pre>'.format(
                open(self.path, 'rU').read()
            )
        elif self.type == 'PDF':
            from wand.image import Image
            import os
            import os.path
            filename_root = self.filename.split('.pdf')[0]
            new_filename = filename_root + '.noteify.png'
            if os.path.exists(self.path.split(self.filename)[0] + new_filename) or os.path.exists(self.path.split(self.filename)[0] + filename_root + '-1.png'):
                pass
            else:
                with Image(filename=self.path, resolution=300) as img:
                    try:
                        img.save(filename=self.path.split(self.filename)[0] + new_filename)
                    except:
                        pass
            self.filename = sorted([filename for filename in os.listdir(self.path.split(self.filename)[0])
                             if filename_root in filename and '.noteify' in filename and '.png' in filename])
            for filename in self.filename:
                html += '<img src="../pdf/{}" height="500" />'.format(filename)
        elif self.type == 'Markdown':
            import markdown
            converter = markdown.Converter()
            html = converter.convert(self.path)
        elif self.type == 'Powerpoint PPTX':
            from comtypes import client
            powerpoint = client.CreateObject('Powerpoint.Application')
            powerpoint.Presentations.Open(self.path)
            powerpoint.ActivePresentation.Export(self.path, 'PNG')
            powerpoint.ActivePresentation.Close()
            powerpoint.Quit()
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
            html = '<table id="{}" style="background-color:rgba(0, 255, 0, 0.2); border:2px solid black; border-collapse:collapse;">'.format(filename)
        else:
            html = '<table id="{}" style="background-color:rgba(0, 255, 0, 0.2); border:2px solid black;">'.format(self.path)
        with open(filename, 'rU') as f:
            c = csv.reader(f)
            for n, row in enumerate(c):
                if n == 0:
                    row_type = 'th'
                    html += '<tr style="background-color:rgba(255, 0, 0, 0.2)"><{} style="padding:4px;">'.format(row_type)
                else:
                    row_type = 'td'
                    html += '<tr><{} style="border:2px; padding:4px;">'.format(row_type)
                joining_string = '</{}><{} style="border:2px; padding:4px;">'.format(row_type, row_type)
                html += joining_string.join(row)
                html += '</{}></tr>'.format(row_type)
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
        self.tags = self.get_tags()
        self.html = self.get_html()

    def get_tags(self):
        t = []
        for f in self.files:
            t += f.tags
        t = sorted(list(set(t)))
        return t

    def get_html(self):
        print 'HTMLifying day', self.date
        html = '<html>' \
               '<head>' \
               '<title>{}</title>' \
               '<link href="http://fonts.googleapis.com/css?family=Lato|PT+Serif|Inconsolata" rel="stylesheet" type="text/css">' \
               '<link href="../style.css" rel="stylesheet" type="text/css" />' \
               '</head>' \
               '<body>' \
               '<h1>{}</h1>'.format(self.date, self.date)
        html += '<h2>Contents</h2><ul>'
        for experiment in self.files:
            if type(experiment.filename) == list:
                html += '<li><a href="#' + experiment.path + '">' + experiment.filename[0].split('.png')[0] + '.pdf</a></li>'
            else:
                html += '<li><a href="#' + experiment.path + '">' + experiment.filename + '</a></li>'
        html += '</ul>'
        for experiment in self.files:
            # print experiment.path, experiment.size
            if type(experiment.filename) != list:
                html += '<h2 id="' + experiment.path + '"><a href="' + experiment.path + '">' + \
                        experiment.filename + '</a></h2>'
            else:
                html += '<h2 id="' + experiment.path + '"><a href="' + experiment.path + '">' + \
                        experiment.filename[0].split('.png')[0] + '.pdf</a></h2>'
            html += '<h4>tags: #' + ', #'.join(experiment.tags) + '</h4>'
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
        import time
        print 'Collating notebook'
        self.days = sorted(day_list, key=lambda x: x.epoch_date, reverse=True)
        self.filename = 'index.html'
        self.epoch_date = time.time()
        self.date = time.asctime(time.localtime(self.epoch_date))

    def __str__(self):
        print self.filename


def html_gen(notebook, outdir):

    import os
    import shutil
    import subprocess

    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if os.path.exists(outdir+'/html'):
        shutil.rmtree(outdir+'/html')
    os.makedirs(outdir+'/html')
    if os.path.exists(outdir+'/img'):
        shutil.rmtree(outdir+'/img')
    os.makedirs(outdir+'/img')
    if os.path.exists(outdir+'/pdf'):
        shutil.rmtree(outdir+'/pdf')
    os.makedirs(outdir+'/pdf')

    shutil.copy('style.css', outdir + '/style.css')

    for day in notebook.days:
        day.write(outdir=outdir+'/html')
        for f in day.files:
            if f.type == 'image':
                try:
                    subprocess.call(['cp', f.path, outdir + '/img/' + f.filename])
                except subprocess.CalledProcessError:
                    pass
            elif f.type == 'PDF':
                for filename in f.filename:
                    try:
                        subprocess.call(['cp', f.path, outdir + '/pdf/' + filename])
                    except subprocess.CalledProcessError:
                        pass

    html = '<html>' \
           '<head>' \
           '<title>Eachan Johnson | Lab Notebook</title>' \
           '<link href="http://fonts.googleapis.com/css?family=Lato|PT+Serif|Inconsolata" rel="stylesheet" type="text/css">' \
           '<link href="style.css" rel="stylesheet" type="text/css" />' \
           '</head>' \
           '<body>' \
           '<h1>Eachan Johnson | Lab Notebook</h1>'
    html += '<h3>Last updated ' + notebook.date + '</h3>'
    html += '<table><tr><th>Date</th><th>Size / MB</th><th>Tags</th><tr>'
    html += '</tr><tr>'.join(['<td><a href="html/{}">{}</a></td><td>{}</td><td style="color:#00ff00;">{}</td>'.format(
        day.filename, day.date, sum([(f.size / 1000000) for f in day.files]), ', '.join(day.tags)
    ) for day in notebook.days])
    html += '</tr></table></body></html>'

    filename = outdir + '/index.html'

    with open(filename, 'w') as f:
        f.write(html)
    return filename