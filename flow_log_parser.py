#!/usr/bin/env python3

import argparse

def read_lookup_table(filename):
    mapping = {}
    with open(filename, 'r') as f:
        header = f.readline()  # Skip header
        for line in f:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            parts = line.split(',')
            if len(parts) != 3:
                continue  # Skip invalid lines
            dstport, protocol, tag = parts
            dstport = dstport.strip()
            protocol = protocol.strip().lower()
            tag = tag.strip().lower()
            key = (dstport, protocol)
            mapping[key] = tag
    return mapping

def process_flow_logs(flow_log_file, mapping):
    tag_counts = {}
    port_protocol_counts = {}

    protocol_map = {
        '1': 'icmp',        
        '2': 'igmp',        
        '6': 'tcp',         
        '17': 'udp',        
        '47': 'gre',        
        '50': 'esp',        
        '51': 'ah',         
        '58': 'icmpv6',     
        '89': 'ospf',       
        '132': 'sctp'
    }

    with open(flow_log_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Skip empty lines and comments
            parts = line.split()
            if len(parts) < 14:
                continue  # Invalid line
            dstport = parts[6]
            protocol_num = parts[7]
            protocol = protocol_map.get(protocol_num, 'other').lower()
            key = (dstport, protocol)

            # For port/protocol counts
            port_protocol_key = (dstport, protocol)
            port_protocol_counts[port_protocol_key] = port_protocol_counts.get(port_protocol_key, 0) + 1

            # For tag counts
            tag = mapping.get(key)
            if tag:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
            else:
                tag_counts['Untagged'] = tag_counts.get('Untagged', 0) + 1

    return tag_counts, port_protocol_counts

def write_output(tag_counts, port_protocol_counts, output_file):
    with open(output_file, 'w') as f:
        f.write('Tag Counts:\n\n')
        f.write('Tag,Count\n')
        for tag, count in tag_counts.items():
            f.write('{},{}\n'.format(tag, count))
        f.write('\nPort/Protocol Combination Counts:\n\n')
        f.write('Port,Protocol,Count\n')
        for (port, protocol), count in port_protocol_counts.items():
            f.write('{},{},{}\n'.format(port, protocol, count))

def main():
    parser = argparse.ArgumentParser(description='Flow Log Parser')
    parser.add_argument('flow_log_file', help='Path to the flow log file')
    parser.add_argument('lookup_file', help='Path to the lookup table file')
    parser.add_argument('output_file', help='Path to the output file')
    args = parser.parse_args()

    mapping = read_lookup_table(args.lookup_file)
    tag_counts, port_protocol_counts = process_flow_logs(args.flow_log_file, mapping)
    write_output(tag_counts, port_protocol_counts, args.output_file)

if __name__ == '__main__':
    main()