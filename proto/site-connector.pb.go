// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.25.0-devel
// 	protoc        v3.14.0
// source: proto/site-connector.proto

package proto

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	reflect "reflect"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

var File_proto_site_connector_proto protoreflect.FileDescriptor

var file_proto_site_connector_proto_rawDesc = []byte{
	0x0a, 0x1a, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x2f, 0x73, 0x69, 0x74, 0x65, 0x2d, 0x63, 0x6f, 0x6e,
	0x6e, 0x65, 0x63, 0x74, 0x6f, 0x72, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x12, 0x05, 0x70, 0x72,
	0x6f, 0x74, 0x6f, 0x1a, 0x1c, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x2f, 0x63, 0x6f, 0x6d, 0x70, 0x75,
	0x74, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x2d, 0x6d, 0x73, 0x67, 0x73, 0x2e, 0x70, 0x72, 0x6f, 0x74,
	0x6f, 0x1a, 0x1d, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x2f, 0x61, 0x76, 0x61, 0x69, 0x6c, 0x61, 0x62,
	0x69, 0x6c, 0x69, 0x74, 0x79, 0x2d, 0x6d, 0x73, 0x67, 0x73, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f,
	0x1a, 0x26, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x2f, 0x73, 0x65, 0x6c, 0x65, 0x63, 0x74, 0x6f, 0x72,
	0x2d, 0x76, 0x65, 0x72, 0x69, 0x66, 0x69, 0x63, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x2d, 0x6d, 0x73,
	0x67, 0x73, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x32, 0xe6, 0x01, 0x0a, 0x0d, 0x53, 0x69, 0x74,
	0x65, 0x43, 0x6f, 0x6e, 0x6e, 0x65, 0x63, 0x74, 0x6f, 0x72, 0x12, 0x3c, 0x0a, 0x03, 0x4d, 0x61,
	0x70, 0x12, 0x16, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x2e, 0x4d, 0x61, 0x70, 0x52, 0x65, 0x71,
	0x75, 0x65, 0x73, 0x74, 0x43, 0x68, 0x75, 0x6e, 0x6b, 0x1a, 0x17, 0x2e, 0x70, 0x72, 0x6f, 0x74,
	0x6f, 0x2e, 0x4d, 0x61, 0x70, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x43, 0x68, 0x75,
	0x6e, 0x6b, 0x22, 0x00, 0x28, 0x01, 0x30, 0x01, 0x12, 0x43, 0x0a, 0x0d, 0x53, 0x69, 0x74, 0x65,
	0x41, 0x76, 0x61, 0x69, 0x6c, 0x61, 0x62, 0x6c, 0x65, 0x12, 0x17, 0x2e, 0x70, 0x72, 0x6f, 0x74,
	0x6f, 0x2e, 0x53, 0x69, 0x74, 0x65, 0x41, 0x76, 0x61, 0x69, 0x6c, 0x61, 0x62, 0x6c, 0x65, 0x52,
	0x65, 0x71, 0x1a, 0x17, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x2e, 0x53, 0x69, 0x74, 0x65, 0x41,
	0x76, 0x61, 0x69, 0x6c, 0x61, 0x62, 0x6c, 0x65, 0x52, 0x65, 0x73, 0x22, 0x00, 0x12, 0x52, 0x0a,
	0x0e, 0x56, 0x65, 0x72, 0x69, 0x66, 0x79, 0x53, 0x65, 0x6c, 0x65, 0x63, 0x74, 0x6f, 0x72, 0x12,
	0x1e, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x2e, 0x53, 0x65, 0x6c, 0x65, 0x63, 0x74, 0x6f, 0x72,
	0x56, 0x65, 0x72, 0x69, 0x66, 0x69, 0x63, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x52, 0x65, 0x71, 0x1a,
	0x1e, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x2e, 0x53, 0x65, 0x6c, 0x65, 0x63, 0x74, 0x6f, 0x72,
	0x56, 0x65, 0x72, 0x69, 0x66, 0x69, 0x63, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x52, 0x65, 0x73, 0x22,
	0x00, 0x42, 0x09, 0x5a, 0x07, 0x2e, 0x3b, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x62, 0x06, 0x70, 0x72,
	0x6f, 0x74, 0x6f, 0x33,
}

var file_proto_site_connector_proto_goTypes = []interface{}{
	(*MapRequestChunk)(nil),         // 0: proto.MapRequestChunk
	(*SiteAvailableReq)(nil),        // 1: proto.SiteAvailableReq
	(*SelectorVerificationReq)(nil), // 2: proto.SelectorVerificationReq
	(*MapResponseChunk)(nil),        // 3: proto.MapResponseChunk
	(*SiteAvailableRes)(nil),        // 4: proto.SiteAvailableRes
	(*SelectorVerificationRes)(nil), // 5: proto.SelectorVerificationRes
}
var file_proto_site_connector_proto_depIdxs = []int32{
	0, // 0: proto.SiteConnector.Map:input_type -> proto.MapRequestChunk
	1, // 1: proto.SiteConnector.SiteAvailable:input_type -> proto.SiteAvailableReq
	2, // 2: proto.SiteConnector.VerifySelector:input_type -> proto.SelectorVerificationReq
	3, // 3: proto.SiteConnector.Map:output_type -> proto.MapResponseChunk
	4, // 4: proto.SiteConnector.SiteAvailable:output_type -> proto.SiteAvailableRes
	5, // 5: proto.SiteConnector.VerifySelector:output_type -> proto.SelectorVerificationRes
	3, // [3:6] is the sub-list for method output_type
	0, // [0:3] is the sub-list for method input_type
	0, // [0:0] is the sub-list for extension type_name
	0, // [0:0] is the sub-list for extension extendee
	0, // [0:0] is the sub-list for field type_name
}

func init() { file_proto_site_connector_proto_init() }
func file_proto_site_connector_proto_init() {
	if File_proto_site_connector_proto != nil {
		return
	}
	file_proto_computation_msgs_proto_init()
	file_proto_availability_msgs_proto_init()
	file_proto_selector_verification_msgs_proto_init()
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_proto_site_connector_proto_rawDesc,
			NumEnums:      0,
			NumMessages:   0,
			NumExtensions: 0,
			NumServices:   1,
		},
		GoTypes:           file_proto_site_connector_proto_goTypes,
		DependencyIndexes: file_proto_site_connector_proto_depIdxs,
	}.Build()
	File_proto_site_connector_proto = out.File
	file_proto_site_connector_proto_rawDesc = nil
	file_proto_site_connector_proto_goTypes = nil
	file_proto_site_connector_proto_depIdxs = nil
}

// Reference imports to suppress errors if they are not otherwise used.
var _ context.Context
var _ grpc.ClientConnInterface

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
const _ = grpc.SupportPackageIsVersion6

// SiteConnectorClient is the client API for SiteConnector service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://godoc.org/google.golang.org/grpc#ClientConn.NewStream.
type SiteConnectorClient interface {
	// Relays a computation request from the coordinator to appropriate algorithm in site
	Map(ctx context.Context, opts ...grpc.CallOption) (SiteConnector_MapClient, error)
	// Pinged by the coordinator to determine whether a site is available
	SiteAvailable(ctx context.Context, in *SiteAvailableReq, opts ...grpc.CallOption) (*SiteAvailableRes, error)
	// Sends a request to the site to verify the selector
	VerifySelector(ctx context.Context, in *SelectorVerificationReq, opts ...grpc.CallOption) (*SelectorVerificationRes, error)
}

type siteConnectorClient struct {
	cc grpc.ClientConnInterface
}

func NewSiteConnectorClient(cc grpc.ClientConnInterface) SiteConnectorClient {
	return &siteConnectorClient{cc}
}

func (c *siteConnectorClient) Map(ctx context.Context, opts ...grpc.CallOption) (SiteConnector_MapClient, error) {
	stream, err := c.cc.NewStream(ctx, &_SiteConnector_serviceDesc.Streams[0], "/proto.SiteConnector/Map", opts...)
	if err != nil {
		return nil, err
	}
	x := &siteConnectorMapClient{stream}
	return x, nil
}

type SiteConnector_MapClient interface {
	Send(*MapRequestChunk) error
	Recv() (*MapResponseChunk, error)
	grpc.ClientStream
}

type siteConnectorMapClient struct {
	grpc.ClientStream
}

func (x *siteConnectorMapClient) Send(m *MapRequestChunk) error {
	return x.ClientStream.SendMsg(m)
}

func (x *siteConnectorMapClient) Recv() (*MapResponseChunk, error) {
	m := new(MapResponseChunk)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func (c *siteConnectorClient) SiteAvailable(ctx context.Context, in *SiteAvailableReq, opts ...grpc.CallOption) (*SiteAvailableRes, error) {
	out := new(SiteAvailableRes)
	err := c.cc.Invoke(ctx, "/proto.SiteConnector/SiteAvailable", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *siteConnectorClient) VerifySelector(ctx context.Context, in *SelectorVerificationReq, opts ...grpc.CallOption) (*SelectorVerificationRes, error) {
	out := new(SelectorVerificationRes)
	err := c.cc.Invoke(ctx, "/proto.SiteConnector/VerifySelector", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// SiteConnectorServer is the server API for SiteConnector service.
type SiteConnectorServer interface {
	// Relays a computation request from the coordinator to appropriate algorithm in site
	Map(SiteConnector_MapServer) error
	// Pinged by the coordinator to determine whether a site is available
	SiteAvailable(context.Context, *SiteAvailableReq) (*SiteAvailableRes, error)
	// Sends a request to the site to verify the selector
	VerifySelector(context.Context, *SelectorVerificationReq) (*SelectorVerificationRes, error)
}

// UnimplementedSiteConnectorServer can be embedded to have forward compatible implementations.
type UnimplementedSiteConnectorServer struct {
}

func (*UnimplementedSiteConnectorServer) Map(SiteConnector_MapServer) error {
	return status.Errorf(codes.Unimplemented, "method Map not implemented")
}
func (*UnimplementedSiteConnectorServer) SiteAvailable(context.Context, *SiteAvailableReq) (*SiteAvailableRes, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SiteAvailable not implemented")
}
func (*UnimplementedSiteConnectorServer) VerifySelector(context.Context, *SelectorVerificationReq) (*SelectorVerificationRes, error) {
	return nil, status.Errorf(codes.Unimplemented, "method VerifySelector not implemented")
}

func RegisterSiteConnectorServer(s *grpc.Server, srv SiteConnectorServer) {
	s.RegisterService(&_SiteConnector_serviceDesc, srv)
}

func _SiteConnector_Map_Handler(srv interface{}, stream grpc.ServerStream) error {
	return srv.(SiteConnectorServer).Map(&siteConnectorMapServer{stream})
}

type SiteConnector_MapServer interface {
	Send(*MapResponseChunk) error
	Recv() (*MapRequestChunk, error)
	grpc.ServerStream
}

type siteConnectorMapServer struct {
	grpc.ServerStream
}

func (x *siteConnectorMapServer) Send(m *MapResponseChunk) error {
	return x.ServerStream.SendMsg(m)
}

func (x *siteConnectorMapServer) Recv() (*MapRequestChunk, error) {
	m := new(MapRequestChunk)
	if err := x.ServerStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func _SiteConnector_SiteAvailable_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(SiteAvailableReq)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(SiteConnectorServer).SiteAvailable(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/proto.SiteConnector/SiteAvailable",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(SiteConnectorServer).SiteAvailable(ctx, req.(*SiteAvailableReq))
	}
	return interceptor(ctx, in, info, handler)
}

func _SiteConnector_VerifySelector_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(SelectorVerificationReq)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(SiteConnectorServer).VerifySelector(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/proto.SiteConnector/VerifySelector",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(SiteConnectorServer).VerifySelector(ctx, req.(*SelectorVerificationReq))
	}
	return interceptor(ctx, in, info, handler)
}

var _SiteConnector_serviceDesc = grpc.ServiceDesc{
	ServiceName: "proto.SiteConnector",
	HandlerType: (*SiteConnectorServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "SiteAvailable",
			Handler:    _SiteConnector_SiteAvailable_Handler,
		},
		{
			MethodName: "VerifySelector",
			Handler:    _SiteConnector_VerifySelector_Handler,
		},
	},
	Streams: []grpc.StreamDesc{
		{
			StreamName:    "Map",
			Handler:       _SiteConnector_Map_Handler,
			ServerStreams: true,
			ClientStreams: true,
		},
	},
	Metadata: "proto/site-connector.proto",
}