import os, re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RES_DIR = os.path.join(BASE_DIR, 'resfiles') # python xingapi 제공
# RES_DIR = r"C:\eBEST\xingAPI\Res" # eBest devcenter 통해 다운로드 받는 경로

class Res:
    def __init__(self, name, res_dir=RES_DIR):
        self.name = name
        self.path = os.path.join(res_dir, self.name+'.res')
        self.blocks, self.code_names, self.code_keys, self.data_types, self.data_sizes, self.data_lengths = self.parse_res(self.path)

    def __call__(self, block_name):
        return self.get(block_name)

    def get(self, block_name):
        block_name = block_name.lower()
        if self.name.lower() in block_name:
            block_name = block_name.replace(self.name.lower(), '')
        for key in self.blocks.keys():
            if block_name in key.lower():
                block_name = key
        block_codes = self.blocks[block_name]
        return block_name, block_codes

    @staticmethod    
    def parse_res(path):
        with open(path, encoding="euc-kr") as f:
            read    = f.read().replace('\t', '')
            data    = re.search(r"BEGIN_DATA_MAP([\S\s]*)END_DATA_MAP", read)
            blocks  = re.findall(r"([\S\s]*?)\sbegin\s([\S\s]*?)\send\s", data.group(1))

        parsed_blocks       = {}
        parsed_code_names   = {}
        parsed_code_keys    = {}
        parsed_data_types   = {}
        parsed_data_sizes   = {}
        parsed_data_lengths = {}
        for block in blocks:
            block_name      = re.sub(' |\n', '', block[0]).split(',')[0]
            block_codes     = {}
            code_names      = []
            code_keys       = []
            data_types      = []
            data_sizes      = []
            data_lengths    = []
            for block_item in list(filter(None, re.sub(' |;', '', block[1]).split('\n'))):
                try:
                    code_name, code_key, _, data_type, data_size = block_item.split(',')
                except:
                    print(block_item)
                block_codes[code_key]   = code_name
                code_names.append(code_name)
                code_keys.append(code_key)
                data_types.append(data_type)
                data_sizes.append(data_size)
                data_lengths.append(int(data_size.split('.')[0]))
            parsed_blocks[block_name]       = block_codes
            parsed_code_names[block_name]   = code_names
            parsed_code_keys[block_name]    = code_keys
            parsed_data_types[block_name]   = data_types
            parsed_data_sizes[block_name]   = data_sizes
            parsed_data_lengths[block_name] = data_lengths

        return parsed_blocks, parsed_code_names, parsed_code_keys, parsed_data_types, parsed_data_sizes, parsed_data_lengths

    def parse_block_request(self, data, by_code_names=True, block_name='OutBlock'):
        data = data.replace(' ', '')
        parsed_dict = {}

        labels = self.code_names[block_name]
        if not by_code_names:
            labels = self.code_keys[block_name]

        for label, length in zip(labels, self.data_lengths[block_name]):
            parsed_dict[label] = data[:length]
            data = data[length:]

        return parsed_dict

if __name__ == "__main__":
    from pprint import pprint
    a = Res('S3_')
    print(a.parse_block_request('1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111112'))
    