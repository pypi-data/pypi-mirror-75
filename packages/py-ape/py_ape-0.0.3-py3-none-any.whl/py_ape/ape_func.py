from tqdm import tqdm
from time import sleep
from tqdm import trange
from bs4 import BeautifulSoup
import pandas as pd
import py_stringsimjoin as ssj
import py_stringmatching as sm
import py_entitymatching as em
from py_entitymatching.catalog import catalog_manager as cm
import flexmatcher
import re
import os
import contextlib
import warnings
warnings.filterwarnings("ignore")
import urllib.request  # Importing urlib (BigGorilla's recommendation for data acquisition from the web)

def is_html_tag(text):
    """
    Check if text contains HTML tags
    :text: The string needs to be checked
    """
    result = re.search(r"<[^>]*>", text)
    # result = re.search(r"<(\w+)\s+\w+.*?>", text)

    if result is None:
      return False
    html_tag = ('doctype', 'a', 'abbr', 'acronym', 'address', 'applet', 'area', 'article', 'aside', 'audio', 'b', 'base',
                'basefont', 'bb', 'bdo', 'big', 'blockquote', 'body', 'br', 'button', 'canvas', 'caption', 'center', 'cite',
                'code', 'col', 'colgroup', 'command', 'datagrid', 'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'dir',
                'div', 'dl', 'dt', 'em', 'embed', 'eventsource', 'fieldset', 'figcaption', 'figure', 'font', 'footer', 'form',
                'frame', 'frameset', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'header', 'hgroup', 'hr', 'html', 'i', 'iframe',
                'img', 'input', 'ins', 'isindex', 'kbd', 'keygen', 'label', 'legend', 'li', 'link', 'map', 'mark', 'menu', 'meta',
                'meter', 'nav', 'noframes', 'noscript', 'object', 'ol', 'optgroup', 'option', 'output', 'p', 'param', 'pre', 'progress',
                'q', 'rp', 'rt', 'ruby', 's', 'samp', 'script', 'section', 'select', 'small', 'source', 'span', 'strike', 'strong', 'style',
                'sub', 'sup', 'table', 'tbody', 'td', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'track', 'tt', 'u', 'ul',
                'var', 'video', 'wbr')
    return result.group().lstrip('<').rstrip('>').lower() in html_tag

def remove_html_tag(text):
  """
  Remove HTML tags using BeautifulSoup package
  :text: The text needs to be removed HTML tags
  """
  return BeautifulSoup(text, 'lxml').get_text()

def count_file_length(fname):
  """
  Count file length for showing progress bar
  :fname: file path
  """
  with open(fname) as f:
    for i, l in enumerate(f):
      pass
  return i + 1

def progress(value, max=100):
    return HTML("""
        <progress
            value='{value}'
            max='{max}',
            style='width: 100%'
        >
            {value}
        </progress>
    """.format(value=value, max=max))

def get_path(file_path):
  """
  Get full path of file_path excepts file name
  :file_path: File path
  """
  return os.path.split(file_path)[0] + "/"

def normalize_text(text):
  """
  Function to normalize the text
  :text: The text needs to be normalized
  """
  text = str(text)
  text = text.lower()
  text = text.replace(',', ' ')
  text = text.replace('-', ' ')
  text = text.replace('/', ' ')
  text = text.replace("'", '')
  text = text.replace(".", '')
  text = text.replace("\r", '')
  return text.strip()

def replace_text(text):
  """
  Replace escape sequences: carriage return and newline
  :text: The text needs to be replaced
  """
  text = str(text)
  text = text.replace("\r", '')
  text = text.replace("\n", " ")
  return text

def read_file(file_name, sep):
  """
  Read the file at file_name location based on pandas package
  :file_name: path of the file needs to be read
  :sep: seperator to split line into columns
  """
  return pd.read_csv(file_name, sep=sep, error_bad_lines=False);

def match_df(left_table, right_table,
             left_key, right_key,
             left_join_attrs, right_join_attrs,
             left_out_attrs, right_out_attrs,
             threshold):
  """
  Match two tables using StringSimJoin.edit_distance_join
  :left_table: first table needs to be match
  :right_table: second table needs to be match
  :left_key: primary key of left_table
  :right_key: primary key of left_table
  :left_join_attrs: attributes of left_table to join to another
  :right_join_attrs: attributes of right_table to join to another
  :left_out_attrs: attributes of left_table to show
  :right_out_attrs: attributes of right_table to show
  :threshold: the number showing that how similar two tables are when they are matching
  """
  return ssj.edit_distance_join(ltable = left_table, 
                                rtable = right_table, 
                                l_key_attr = left_key, 
                                r_key_attr = right_key, 
                                l_join_attr = left_join_attrs, 
                                r_join_attr = right_join_attrs,
                                comp_op='=',
                                l_out_attrs = left_out_attrs,
                                r_out_attrs = right_out_attrs,
                                threshold = threshold)
def count_duplicate(table, col_names = None):
  """
  Count number of duplicate lines with col_names in table
  :table: dataframe needs to be counted
  :col_names: list of column name in the table. default is None
  """
  if col_names is None:
    return sum(table.duplicated(subset=list(table), keep=False))
  return sum(table.duplicated(subset=col_names, keep=False))

def remove_duplicate(table, col_names = None):
  """
  Remove duplicate lines with col_names in table
  :table: dataframe needs to be counted
  :col_names: list of column name in the table. default is None
  """
  if col_names is None:
    return table.drop_duplicates(subset=list(table), keep='first', inplace=True)
  return table.drop_duplicates(subset=col_names, keep='first', inplace=True)

def evaluate_jaccard(table1, table2, col_name):
  """
  Evaluate similarity score of two tables with col_name using Jaccard
  :table1: first dataframe needs to be evaluated
  :table2: second dataframe needs to be evaluated
  :col_name: column name in the first table to evaluate with all column names in table2
  """
  col_vals = set(table1[col_name].unique())
  column = None
  match_point = 0
  for col in table2.columns:
      ext_col_vals = set(table2[col].unique())
      intersection_size = len(col_vals.intersection(ext_col_vals))
      union_size = len(col_vals.union(ext_col_vals))
      jaccard = intersection_size / union_size
      if jaccard != 0 and jaccard > match_point:
        column = col
        match_point = jaccard
        print(col + ' has similarity score ' + str(jaccard))
  return column

def predict_columns(dataframe1, dataframe2, sample_size=500):
  """
  Predict match columns of two dataframe to the user based on flexmatcher
  :dataframe1: first dataframe needs to be predict
  :dataframe2: second dataframe needs to be predict
  :sample_size: size of samples for the machine to train, default is 500
  """
  schema_list = [dataframe1]
  mapping_list = [dict(zip(dataframe1.columns, dataframe1.columns))]
  fm = flexmatcher.FlexMatcher(schema_list, mapping_list, sample_size)
  fm.train()
  # making a prediction
  return fm.make_prediction(dataframe2)

def export_csv(dataframe, out_path):
  """
  Export the dataframe to csv file with out_path
  :dataframe: dataframe needs to be exported
  :out_path: file path to export
  """
  dataframe.to_csv(out_path, encoding='utf-8')

def read_csv(file_path, sep=','):
  """
  Read the csv file by default, if not, read the file with sep to split line into columns then write log if error happens
  :file_path: file path to read
  :sep: seperator when file is not csv, default is a comma
  """
  with open(get_path(file_path) + 'log.txt', 'w') as log:
    with contextlib.redirect_stderr(log):
        return pd.read_csv(file_path, index_col=False, encoding='iso-8859-1', sep=sep,
                                warn_bad_lines=True, error_bad_lines=False)
        
def mapping_data(data, old_col, new_col, method_to_map):
    """
    Modify the data with method
    :old_col: old column name
    :new_col: new column name
    :method_to_map: the method to map data
    """
    data[new_col] = data[old_col].map(method_to_map)
    return data

def download_file(file_url, file_name, local_path):
    """
    Handle downloading file
    :file_url: url of file
    :file_name: file name to save
    :local_path: the path to save file
    """
    if not os.path.exists(local_path + file_name):  # avoid downloading if the file exists
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64)'
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(file_url, local_path + file_name)
    with open(local_path + file_name) as f:
        line = f.readline()
        if line.startswith('<!DOCTYPE'):
            print('Man-in-the-Middle hampered with download: {}'.format(file_url))
            print('Maybe try to download in browser and copy to subdirectory data.')
        return

def handle_raw_html(input_path, output_path, loop_time):
  """
  Handle processing raw HTML and write it into a new file
  :input_path: path of input file
  :output_path: path of output file
  :loop_time: time to loop for getting text inside HTML tags in a line when BeautifulSoup cannot do it in the first time
  """
  f = open(output_path, "w+")
  f_tag = open(get_path(output_path) + "cant_remove_html.txt", "w+")
  i=1
  line_tag_count = 0
  with open(input_path, "r") as infile:
      file_line_length = count_file_length(input_path)
      pbar = tqdm(total=file_line_length)
      for line in infile:
        soup = remove_html_tag(line.replace("\r", ''))
        i += 1
        pbar.update()
        j = 0
        #loop 10 times
        while is_html_tag(soup) and j < loop_time:
          soup = remove_html_tag(line)
          j += 1
        if is_html_tag(soup):
          line_tag_count +=1
          f_tag.write(soup)
        f.write(soup)
      pbar.close()

  f.close()
  f_tag.close()
  print("\nFound %s lines that cant remove html tags" % line_tag_count)