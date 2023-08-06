import re  # To use regular expressions
import subprocess  # To run shell commands
import time

from lxml import etree  # To read an write XML files


def timeit(method):
    """Time functions."""

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r %2.2f sec' % \
              (method.__name__, te - ts))
        return result

    return timed


class freelingWrapper(object):
    """Wrap FreeLing."""

    @timeit
    def __init__(self, port):
        """Instantiate a wrapper."""

        self.port = port

    def read_xml(self, infile):
        """Parse a XML file."""
        parser = etree.XMLParser(remove_blank_text=True)
        with open(infile, encoding='utf-8', mode='r') as input:
            return etree.parse(input, parser)

    def process_with_freeling(self, itext):
        """Process a string with FreeLing.

        Keyword arguments:
        itext -- a string containing input text to be processed
        """
        itext = re.sub(r'\"', r'\\"', itext)  # scape double quotation marks
        command = 'echo "{}" | analyzer_client {}'.format(  # create command string
            itext,
            self.port)
        process = subprocess.Popen(  # declare process
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True)
        otext, error = process.communicate()  # run process
        otext = otext.decode("utf-8").strip()
        return otext

    # for CWB encoding is not a problem if the XML is pretty,
    # there is an option to cope with it at encoding
    def unprettify(self, tree):
        """Remove any indentation introduced by pretty print."""
        tree = etree.tostring(  # convert XML tree to string
            tree,
            encoding="utf-8",
            method="xml",
            xml_declaration=True).decode()
        tree = re.sub(  # remove trailing spaces before tag
            r"(\n) +(<)",
            r"\1\2",
            tree)
        tree = re.sub(  # put each XML element in a different line
            r"> *<",
            r">\n<",
            tree)
        tree = re.sub(  # put opening tag and FL output in different lines
            r"(<{}.+?>)".format(self.element),
            r"\1\n",
            tree)
        tree = re.sub(  # put FL output and closing tag in different liens
            r"(</{}>)".format(self.element),
            r"\n\1",
            tree)
        tree = re.sub(
            r"(>)([^.])",
            r"\1\n\2",
            tree)
        tree = re.sub(  # remove unnecessary empty lines
            r"\n\n+",
            r"\n",
            tree)
        return tree

    def flg_to_vrt(self, tree):
        """Transform FreeLing output to VRT."""
        if self.sentence == True:
            sentences = tree.findall('.//{}'.format(self.element))
        else:
            sentences = tree.findall('.//s')
        for sentence in sentences:
            sentence.text = re.sub(r' ', r'\t', sentence.text)  # to get VRT directly
            sentence.text = re.sub(r'\t\d(\.\d+)?$', r'', sentence.text, flags=re.MULTILINE)  # to remove probability
        pass

    def get_leafs(self, sentence):
        """Get leaf nodes from constituency tree.

        Keyword arguments:
        sentence -- XML element containing a parsed sentence
        """
        counter = 0
        nodes = sentence.find('./constituents/node')
        s = etree.Element('s')
        s.append(nodes)
        leafs = s.findall('.//node[@leaf]')
        for leaf in leafs:
            ancestors = leaf.iterancestors(tag='node')
            depth = sum([1 for x in ancestors])
            if re.match(r'.+_.+', leaf.attrib['word']):
                words = leaf.attrib['word'].split('_')
                leaf.attrib['word'] = words[0]
                leaf.attrib['token'] = 't_' + str(counter)
                leaf.attrib['depth'] = str(depth)
                leaf.text = '\n{}\n'.format(words[0])
                counter += 1
                parent = leaf.getparent()
                leaf_counter = 2
                for word in words[1:]:
                    child = etree.SubElement(parent, 'node')
                    child.text = '\n{}\n'.format(word)
                    child.attrib['leaf'] = str(leaf_counter)
                    leaf_counter += 1
                    child.attrib['token'] = 't_' + str(counter)
                    counter += 1
                    child.attrib['word'] = word
                    child.attrib['depth'] = str(depth)
                    if 'head' in leaf.attrib:
                        child.attrib['head'] = leaf.attrib['head']
            else:
                leaf.text = '\n{}\n'.format(leaf.attrib['word'])
                leaf.attrib['depth'] = str(depth)
                leaf.attrib['token'] = 't_' + str(counter)
                counter += 1
        return s

    def get_constituency(self, element):
        """Get constituency parsing of the text contained in a XML element.

        Keyword arguments:
        element -- XML element containing text to be parsed.
        """
        analysis = self.process_with_freeling(element.text.strip('\n'))
        analysis = etree.fromstring('<analysis>' + analysis.strip('\n') + '</analysis>')
        if self.sentence is True:
            sentence = analysis.find('.//sentence')
            element.text = None
            parsed_sentence = self.get_leafs(sentence)
            element.getparent().replace(element, parsed_sentence)
        else:
            sentences = analysis.findall('.//sentence')
            new_sentences = []
            for sentence in sentences:
                new_sentences.append(self.get_leafs(sentence))
            element.text = None
            for new_sentence in new_sentences:
                element.append(new_sentence)

    def process_sentences(self, sentences):
        processed = []
        for s in sentences:
            processed.append(self.process_with_freeling(
                s.strip('\n')))

        return processed

# tagger=freelingWrapper(50101)
