import argparse
import yaml
import json
import os.path
import markdown2

def append_to_json(obj, fpath):
    with open(fpath, 'r') as f:
        cnt = json.load(f)
    cnt.append(obj)
    with open(fpath, 'w') as f:
        json.dump(cnt, f, indent=4)

def make_content_obj(co_name):
    return {
        "_id": "co-" + co_name.replace(' ', '-'),
        "_parentId": "course",
        "_type": "page",
        "_classes": "",
        "_htmlClasses": "",
        "title": co_name,
        "displayTitle": co_name,
        "body": None,
        "pageBody": None,
        "instruction": None,
        "_graphic": None,
        "linkText": "View",
        "duration": "5 mins",
        "_pageLevelProgress": {
            "_isEnabled": True,
            "_showPageCompletion": False,
            "_excludeAssessments": False,
            "_isCompletionIndicatorEnabled": False
        }
    }

def make_article(article_name, co_name):
    return {
        "_id": 'a-' + article_name.replace(' ', '-'),
        "_parentId": "co-" + co_name.replace(' ', '-'),
        "_type": "article",
        "_classes": "",
        "title": None,
        "displayTitle": None,
        "body": "",
        "instruction": ""
    }

def make_block(idx, block_name, article_name):
    b_id = "b-" + block_name.replace(' ', '-') + "-" + str(idx)
    return {
        "_id": b_id,
        "_parentId": 'a-' + article_name.replace(' ', '-'),
        "_type": "block",
        "_classes": "",
        "title": b_id,
        "displayTitle": block_name,
        "body": "",
        "instruction": "",
        "_trackingId": idx
    }

def make_component(idx, block_name):
    suf = block_name.replace(' ', '-') + "-" + str(idx)
    c_id = "c-" + suf
    b_id = "b-" + suf
    return {
        "_id": c_id,
        "_parentId": b_id,
        "_type": "component",
        "_component": "text",
        "_classes": "",
        "_layout": "full",
        "title": block_name,
        "displayTitle": None,
        "instruction": None,
        "_pageLevelProgress": {
            "_isEnabled": True
        }
    }

def create_content_object(adapt_dir, md_dir, co_name):
    co_file = os.path.join(adapt_dir, 'src', 'course', 'en', 'contentObjects.json')
    article_file = os.path.join(adapt_dir, 'src', 'course', 'en', 'articles.json')
    block_file = os.path.join(adapt_dir, 'src', 'course', 'en', 'blocks.json')
    component_file = os.path.join(adapt_dir, 'src', 'course', 'en', 'components.json')
    md_yaml = yaml.load(open(os.path.join(md_dir, 'mkdocs.yml')), Loader=yaml.BaseLoader)

    with open(block_file, 'r') as f:
        blocks = json.load(f)
        if blocks:
            cur_bid = blocks[-1]['_trackingId'] + 1
        else:
            cur_bid = 1

    all_files = [i for i in md_yaml['nav'] if co_name in i.keys()]
    subj_to_files = list()
    for comp_to_files in all_files:
        for subj_to_file in list(comp_to_files.values())[0]:
            subj_to_files.append(tuple(list(subj_to_file.items())[0]))
    
    print('Adding content object: ' + co_name)
    append_to_json(make_content_obj(co_name), co_file)

    article_name = co_name
    print('Adding article: ' + article_name)
    append_to_json(make_article(article_name, co_name), article_file)

    for block_name, md_relpath in subj_to_files:
        md_path = os.path.join(md_dir, 'docs', md_relpath)
        with open(md_path, 'r') as f:
            md_block = f.read()

        print('Adding block: ' + block_name + '...')
        md_block = md_block.replace('../assets/', 'course/en/images/')
        append_to_json(make_block(cur_bid, block_name, article_name), block_file)
        component = make_component(cur_bid, block_name)
        component['body'] = markdown2.markdown(md_block)
        append_to_json(component, component_file)
        cur_bid += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('md_dir', help='markdown directory')
    parser.add_argument('adapt_dir', help='Adapt course directory')
    parser.add_argument('co_names', help='name of content objects to add to course (ie. Lecture)', nargs='+')
    args = parser.parse_args()

    for co_name in args.co_names:
        create_content_object(args.adapt_dir, args.md_dir, co_name)
