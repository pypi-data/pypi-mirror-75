# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

mastodon_edge = {
    'color': {
        'color': '#119BDD'
    },
    'title': 'TickTok Snowflake',
    'label': 'tk'
}


def parse_tiktok_snowflake(unfurl, node):
    # Ref: https://github.com/tootsuite/mastodon/issues/1059
    #      https://github.com/tootsuite/mastodon/blob/master/lib/mastodon/snowflake.rb
    try:
        snowflake = int(node.value)
        # Snowflake is 63 bits long; the upper 31 bits are the timestamp.
        # Shift it 32 (63-32 = 31) bits right, leaving just the timestamp bits.
        timestamp = (snowflake >> 32)

    except Exception as e:
        print(e)
        return

    node.hover = 'Mastodon Snowflakes are time-based IDs similar to those of Twitter Snowflakes. ' \
                 '<a href="https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake.html" ' \
                 'target="_blank">[ref]</a>'

    unfurl.add_to_queue(
        data_type='epoch-seconds', key=None, value=timestamp, label=f'Timestamp: {timestamp}',
        hover='The first 16 bits value in a Mastodon Snowflake is a timestamp.',
        parent_id=node.node_id, incoming_edge_config=mastodon_edge)

    unfurl.add_to_queue(
         data_type='integer', key=None, value=seq_data, label=f'Sequence data: {seq_data}',
         hover="The 'sequence data' is intended to be unique within a given millisecond. It is a 2 bytes value.",
         parent_id=node.node_id, incoming_edge_config=mastodon_edge)


def run(unfurl, node):

    if node.data_type == 'url.path.segment':

        # Check if node is a child of a mastodon domain, is an integer, & timestamp would be between 2015-01 and 2030-01
        if 'tiktok.com' in unfurl.find_preceding_domain(node) and \
                unfurl.check_if_int_between(node.value, 6008518692986686725, 7008518692986686725):
            parse_tiktok_snowflake(unfurl, node)
