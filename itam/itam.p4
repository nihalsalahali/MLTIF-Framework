/*-----------------------------------------------------------------------------
 * MLTIF - ITAM Module P4 Program (itam.p4)
 * Based on FLARE (flare_sffp.p4) structure
 * Extracts TCP flags, entropy-related features, flow stats
 * Target: BMv2 (P4_16)
 *---------------------------------------------------------------------------*/

#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_IPV4 = 0x0800;

header ethernet_t {
    bit<48> dst_addr;
    bit<48> src_addr;
    bit<16> ether_type;
}

header ipv4_t {
    bit<4>  version;
    bit<4>  ihl;
    bit<8>  diffserv;
    bit<16> total_len;
    bit<16> identification;
    bit<3>  flags;
    bit<13> frag_offset;
    bit<8>  ttl;
    bit<8>  protocol;
    bit<16> hdr_checksum;
    bit<32> src_addr;
    bit<32> dst_addr;
}

header tcp_t {
    bit<16> src_port;
    bit<16> dst_port;
    bit<32> seq_no;
    bit<32> ack_no;
    bit<4>  data_offset;
    bit<4>  res;
    bit<8>  flags;
    bit<16> window;
    bit<16> checksum;
    bit<16> urgent_ptr;
}

header udp_t {
    bit<16> src_port;
    bit<16> dst_port;
    bit<16> length;
    bit<16> checksum;
}

struct metadata_t {
    bit<1> is_valid;
}

struct headers {
    ethernet_t ethernet;
    ipv4_t     ipv4;
    tcp_t      tcp;
    udp_t      udp;
}

parser ParserImpl(packet_in packet,
                  out headers hdr,
                  inout metadata_t meta,
                  inout standard_metadata_t standard_metadata) {
    state start {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.ether_type) {
            TYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol) {
            6: parse_tcp;
            17: parse_udp;
            default: accept;
        }
    }

    state parse_tcp {
        packet.extract(hdr.tcp);
        transition accept;
    }

    state parse_udp {
        packet.extract(hdr.udp);
        transition accept;
    }
}

control IngressImpl(inout headers hdr,
                    inout metadata_t meta,
                    inout standard_metadata_t standard_metadata) {
    apply {
        if (hdr.ipv4.isValid()) {
            // Basic entropy-related indicators
            // These would be read/exported to control plane
            // via registers or digest messages (not shown here)
            bit<8> proto = hdr.ipv4.protocol;
            bit<8> ttl = hdr.ipv4.ttl;

            if (hdr.tcp.isValid()) {
                bit<8> tcp_flags = hdr.tcp.flags;
                bit<16> payload_size = hdr.ipv4.total_len - (hdr.ipv4.ihl * 4) - (hdr.tcp.data_offset * 4);
            } else if (hdr.udp.isValid()) {
                bit<16> udp_len = hdr.udp.length;
            }
        }
    }
}

control EgressImpl(inout headers hdr,
                   inout metadata_t meta,
                   inout standard_metadata_t standard_metadata) {
    apply { }
}

control DeparserImpl(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        if (hdr.tcp.isValid()) {
            packet.emit(hdr.tcp);
        } else if (hdr.udp.isValid()) {
            packet.emit(hdr.udp);
        }
    }
}

V1Switch(ParserImpl(), IngressImpl(), EgressImpl(), DeparserImpl()) {}
