from pathlib import Path
import xml.etree.ElementTree as xml_tree

import yaml


def _get_items(yaml_data):
    raw_items = yaml_data.get('items', yaml_data.get('item', []))
    if isinstance(raw_items, dict):
        return [raw_items]
    return raw_items or []


def build_feed(yaml_data):
    rss_element = xml_tree.Element(
        'rss',
        {
            'version': '2.0',
            'xmlns:itunes': 'https://www.itunes.com/dtds/podcast-1.0.dtd',
            'xmlns:content': 'http://purl.org/rss/1.0/modules/content/',
        },
    )

    link_prefix = yaml_data.get('link_prefix', '')
    channel_element = xml_tree.SubElement(rss_element, 'channel')

    xml_tree.SubElement(channel_element, 'title').text = yaml_data.get('title', '')
    if yaml_data.get('subtitle'):
        xml_tree.SubElement(channel_element, 'subtitle').text = yaml_data['subtitle']
    if yaml_data.get('author'):
        xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
    if yaml_data.get('description'):
        xml_tree.SubElement(channel_element, 'description').text = yaml_data['description']
    if yaml_data.get('image'):
        xml_tree.SubElement(channel_element, 'itunes:image', {'href': yaml_data['image']})
    if yaml_data.get('language'):
        xml_tree.SubElement(channel_element, 'language').text = yaml_data['language']
    if yaml_data.get('link'):
        link_value = yaml_data['link']
        xml_tree.SubElement(channel_element, 'link').text = f'{link_prefix}/{link_value}' if link_prefix else link_value
    if yaml_data.get('category'):
        xml_tree.SubElement(channel_element, 'itunes:category', {'text': yaml_data['category']})

    for item in _get_items(yaml_data):
        item_element = xml_tree.SubElement(channel_element, 'item')
        if item.get('title'):
            xml_tree.SubElement(item_element, 'title').text = item['title']
        if item.get('description'):
            xml_tree.SubElement(item_element, 'description').text = item['description']
        if item.get('pubDate'):
            xml_tree.SubElement(item_element, 'pubDate').text = item['pubDate']
        if item.get('author'):
            xml_tree.SubElement(item_element, 'itunes:author').text = item['author']
        if item.get('duration'):
            xml_tree.SubElement(item_element, 'itunes:duration').text = item['duration']
        if item.get('link'):
            enclosure_url = f'{link_prefix}/{item["link"]}' if link_prefix else item['link']
            xml_tree.SubElement(
                item_element,
                'enclosure',
                {
                    'url': enclosure_url,
                    'length': str(item.get('length', 0)),
                    'type': item.get('type', 'audio/mpeg'),
                },
            )

    return rss_element


def write_feed(output_path, yaml_data):
    output_tree = xml_tree.ElementTree(build_feed(yaml_data))
    output_tree.write(output_path, encoding='UTF-8', xml_declaration=True)


def main():
    with open('feed.yaml', 'r', encoding='utf-8') as file:
        yaml_data = yaml.safe_load(file)

    write_feed(Path('podcast.xml'), yaml_data)


if __name__ == '__main__':
    main()
