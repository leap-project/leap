/**
 * @fileoverview gRPC-Web generated client stub for protoBuf
 * @enhanceable
 * @public
 */

/* eslint-disable */
// GENERATED CODE -- DO NOT EDIT!



const grpc = {};
grpc.web = require('grpc-web');


var computation$msgs_pb = require('./computation-msgs_pb.js')
const proto = {};
proto.protoBuf = require('./cloud-algos_pb.js');

/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?Object} options
 * @constructor
 * @struct
 * @final
 */
proto.protoBuf.CloudAlgoClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options['format'] = 'text';

  /**
   * @private @const {!grpc.web.GrpcWebClientBase} The client
   */
  this.client_ = new grpc.web.GrpcWebClientBase(options);

  /**
   * @private @const {string} The hostname
   */
  this.hostname_ = hostname;

};


/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?Object} options
 * @constructor
 * @struct
 * @final
 */
proto.protoBuf.CloudAlgoPromiseClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options['format'] = 'text';

  /**
   * @private @const {!grpc.web.GrpcWebClientBase} The client
   */
  this.client_ = new grpc.web.GrpcWebClientBase(options);

  /**
   * @private @const {string} The hostname
   */
  this.hostname_ = hostname;

};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.protoBuf.ComputeRequest,
 *   !proto.protoBuf.ComputeResponse>}
 */
const methodDescriptor_CloudAlgo_Compute = new grpc.web.MethodDescriptor(
  '/protoBuf.CloudAlgo/Compute',
  grpc.web.MethodType.UNARY,
  computation$msgs_pb.ComputeRequest,
  computation$msgs_pb.ComputeResponse,
  /**
   * @param {!proto.protoBuf.ComputeRequest} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  computation$msgs_pb.ComputeResponse.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.protoBuf.ComputeRequest,
 *   !proto.protoBuf.ComputeResponse>}
 */
const methodInfo_CloudAlgo_Compute = new grpc.web.AbstractClientBase.MethodInfo(
  computation$msgs_pb.ComputeResponse,
  /**
   * @param {!proto.protoBuf.ComputeRequest} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  computation$msgs_pb.ComputeResponse.deserializeBinary
);


/**
 * @param {!proto.protoBuf.ComputeRequest} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.protoBuf.ComputeResponse)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.protoBuf.ComputeResponse>|undefined}
 *     The XHR Node Readable Stream
 */
proto.protoBuf.CloudAlgoClient.prototype.compute =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/protoBuf.CloudAlgo/Compute',
      request,
      metadata || {},
      methodDescriptor_CloudAlgo_Compute,
      callback);
};


/**
 * @param {!proto.protoBuf.ComputeRequest} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.protoBuf.ComputeResponse>}
 *     A native promise that resolves to the response
 */
proto.protoBuf.CloudAlgoPromiseClient.prototype.compute =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/protoBuf.CloudAlgo/Compute',
      request,
      metadata || {},
      methodDescriptor_CloudAlgo_Compute);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.protoBuf.ComputeRequest,
 *   !proto.protoBuf.ComputeResponse>}
 */
const methodDescriptor_CloudAlgo_WebRequest = new grpc.web.MethodDescriptor(
  '/protoBuf.CloudAlgo/WebRequest',
  grpc.web.MethodType.UNARY,
  computation$msgs_pb.ComputeRequest,
  computation$msgs_pb.ComputeResponse,
  /**
   * @param {!proto.protoBuf.ComputeRequest} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  computation$msgs_pb.ComputeResponse.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.protoBuf.ComputeRequest,
 *   !proto.protoBuf.ComputeResponse>}
 */
const methodInfo_CloudAlgo_WebRequest = new grpc.web.AbstractClientBase.MethodInfo(
  computation$msgs_pb.ComputeResponse,
  /**
   * @param {!proto.protoBuf.ComputeRequest} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  computation$msgs_pb.ComputeResponse.deserializeBinary
);


/**
 * @param {!proto.protoBuf.ComputeRequest} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.protoBuf.ComputeResponse)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.protoBuf.ComputeResponse>|undefined}
 *     The XHR Node Readable Stream
 */
proto.protoBuf.CloudAlgoClient.prototype.webRequest =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/protoBuf.CloudAlgo/WebRequest',
      request,
      metadata || {},
      methodDescriptor_CloudAlgo_WebRequest,
      callback);
};


/**
 * @param {!proto.protoBuf.ComputeRequest} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.protoBuf.ComputeResponse>}
 *     A native promise that resolves to the response
 */
proto.protoBuf.CloudAlgoPromiseClient.prototype.webRequest =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/protoBuf.CloudAlgo/WebRequest',
      request,
      metadata || {},
      methodDescriptor_CloudAlgo_WebRequest);
};


module.exports = proto.protoBuf;

