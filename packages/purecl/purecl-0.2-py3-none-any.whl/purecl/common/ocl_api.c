typedef int32_t cl_int;
    typedef uint32_t cl_uint;
    typedef uint64_t cl_ulong;
    typedef uint64_t cl_device_type;
    typedef uint32_t cl_platform_info;
    typedef uint32_t cl_device_info;
    typedef uint32_t cl_program_build_info;
    typedef cl_uint  cl_program_info;
    typedef cl_uint  cl_kernel_info;
    typedef uint32_t cl_kernel_work_group_info;
    typedef uint32_t cl_command_queue_properties;
    typedef uint32_t cl_command_queue_info;
    typedef uint64_t cl_queue_properties;
    typedef uint64_t cl_mem_flags;
    typedef uint32_t cl_bool;
    typedef uint64_t cl_map_flags;
    typedef uint32_t cl_profiling_info;
    typedef uint32_t cl_buffer_create_type;
    typedef uint64_t cl_svm_mem_flags;
    typedef uint32_t cl_event_info;

    typedef void* cl_platform_id;
    typedef void* cl_device_id;
    typedef void* cl_context;
    typedef void* cl_program;
    typedef void* cl_kernel;
    typedef void* cl_command_queue;
    typedef void* cl_mem;
    typedef void* cl_event;

    typedef intptr_t cl_context_properties;
    typedef intptr_t cl_pipe_properties;

    cl_int clGetPlatformIDs(cl_uint num_entries,
                            cl_platform_id *platforms,
                            cl_uint *num_platforms);
    cl_int clGetDeviceIDs(cl_platform_id  platform,
                          cl_device_type device_type,
                          cl_uint num_entries,
                          cl_device_id *devices,
                          cl_uint *num_devices);

    cl_int clGetPlatformInfo(cl_platform_id platform,
                             cl_platform_info param_name,
                             size_t param_value_size,
                             void *param_value,
                             size_t *param_value_size_ret);
    cl_int clGetDeviceInfo(cl_device_id device,
                           cl_device_info param_name,
                           size_t param_value_size,
                           void *param_value,
                           size_t *param_value_size_ret);

    cl_context clCreateContext(const cl_context_properties *properties,
                               cl_uint num_devices,
                               const cl_device_id *devices,
                               void *pfn_notify,
                               void *user_data,
                               cl_int *errcode_ret);
    cl_int clReleaseContext(cl_context context);

    cl_program clCreateProgramWithSource(cl_context context,
                                         cl_uint count,
                                         const char **strings,
                                         const size_t *lengths,
                                         cl_int *errcode_ret);

    cl_program clCreateProgramWithBinary(cl_context context,
                                         cl_uint num_devices,
                                         const cl_device_id *device_list,
                                         const size_t *lengths,
                                         const unsigned char **binaries,
                                         cl_int *binary_status,
                                         cl_int *errcode_ret);

    cl_int clReleaseProgram(cl_program program);
    cl_int clBuildProgram(cl_program program,
                          cl_uint num_devices,
                          const cl_device_id *device_list,
                          const char *options,
                          void *pfn_notify,
                          void *user_data);
    cl_int clGetProgramBuildInfo(cl_program program,
                                 cl_device_id device,
                                 cl_program_build_info param_name,
                                 size_t param_value_size,
                                 void *param_value,
                                 size_t *param_value_size_ret);

    cl_int clGetProgramInfo(cl_program program,
                            cl_program_info param_name,
                            size_t param_value_size,
                            void *param_value,
                            size_t *param_value_size_ret);

    cl_kernel clCreateKernel(cl_program program,
                             const char *kernel_name,
                             cl_int *errcode_ret);
    cl_int clReleaseKernel(cl_kernel kernel);
    cl_int clGetKernelInfo(cl_kernel kernel,
                           cl_kernel_info param_name,
                           size_t param_value_size,
                           void *param_value,
                           size_t *param_value_size_ret);

    cl_int clGetKernelWorkGroupInfo(cl_kernel kernel,
                                    cl_device_id device,
                                    cl_kernel_work_group_info param_name,
                                    size_t param_value_size,
                                    void *param_value,
                                    size_t *param_value_size_ret);
    cl_int clSetKernelArg(cl_kernel kernel,
                          cl_uint arg_index,
                          size_t arg_size,
                          const void *arg_value);

    cl_command_queue clCreateCommandQueue(
                                    cl_context context,
                                    cl_device_id device,
                                    cl_command_queue_properties properties,
                                    cl_int *errcode_ret);
    cl_command_queue clCreateCommandQueueWithProperties(
                                    cl_context context,
                                    cl_device_id device,
                                    const cl_queue_properties *properties,
                                    cl_int *errcode_ret);
    cl_int clReleaseCommandQueue(cl_command_queue command_queue);

    cl_mem clCreateBuffer(cl_context context,
                          cl_mem_flags flags,
                          size_t size,
                          void *host_ptr,
                          cl_int *errcode_ret);
    cl_mem clCreateSubBuffer(cl_mem buffer,
                             cl_mem_flags flags,
                             cl_buffer_create_type buffer_create_type,
                             const void *buffer_create_info,
                             cl_int *errcode_ret);
    cl_int clReleaseMemObject(cl_mem memobj);
    void* clEnqueueMapBuffer(cl_command_queue command_queue,
                             cl_mem buffer,
                             cl_bool blocking_map,
                             cl_map_flags map_flags,
                             size_t offset,
                             size_t size,
                             cl_uint num_events_in_wait_list,
                             const cl_event *event_wait_list,
                             cl_event *event,
                             cl_int *errcode_ret);
    cl_int clEnqueueUnmapMemObject(cl_command_queue command_queue,
                                   cl_mem memobj,
                                   void *mapped_ptr,
                                   cl_uint num_events_in_wait_list,
                                   const cl_event *event_wait_list,
                                   cl_event *event);
    cl_int clEnqueueReadBuffer(cl_command_queue command_queue,
                               cl_mem buffer,
                               cl_bool blocking_read,
                               size_t offset,
                               size_t size,
                               void *ptr,
                               cl_uint num_events_in_wait_list,
                               const cl_event *event_wait_list,
                               cl_event *event);
    cl_int clEnqueueWriteBuffer(cl_command_queue command_queue,
                                cl_mem buffer,
                                cl_bool blocking_write,
                                size_t offset,
                                size_t size,
                                const void *ptr,
                                cl_uint num_events_in_wait_list,
                                const cl_event *event_wait_list,
                                cl_event *event);
    cl_int clEnqueueCopyBuffer(cl_command_queue command_queue,
                               cl_mem src_buffer,
                               cl_mem dst_buffer,
                               size_t src_offset,
                               size_t dst_offset,
                               size_t size,
                               cl_uint num_events_in_wait_list,
                               const cl_event *event_wait_list,
                               cl_event *event);
    cl_int clEnqueueCopyBufferRect(cl_command_queue command_queue,
                                   cl_mem src_buffer,
                                   cl_mem dst_buffer,
                                   const size_t *src_origin,
                                   const size_t *dst_origin,
                                   const size_t *region,
                                   size_t src_row_pitch,
                                   size_t src_slice_pitch,
                                   size_t dst_row_pitch,
                                   size_t dst_slice_pitch,
                                   cl_uint num_events_in_wait_list,
                                   const cl_event *event_wait_list,
                                   cl_event *event);
    cl_int clEnqueueFillBuffer(cl_command_queue command_queue,
                               cl_mem buffer,
                               const void *pattern,
                               size_t pattern_size,
                               size_t offset,
                               size_t size,
                               cl_uint num_events_in_wait_list,
                               const cl_event *event_wait_list,
                               cl_event *event);

    cl_int clWaitForEvents(cl_uint num_events,
                           const cl_event *event_list);
    cl_int clReleaseEvent(cl_event event);

    cl_int clFlush(cl_command_queue command_queue);
    cl_int clFinish(cl_command_queue command_queue);

    cl_int clEnqueueNDRangeKernel(cl_command_queue command_queue,
                                  cl_kernel kernel,
                                  cl_uint work_dim,
                                  const size_t *global_work_offset,
                                  const size_t *global_work_size,
                                  const size_t *local_work_size,
                                  cl_uint num_events_in_wait_list,
                                  const cl_event *event_wait_list,
                                  cl_event *event);

    cl_int clGetEventProfilingInfo(cl_event event,
                                   cl_profiling_info param_name,
                                   size_t param_value_size,
                                   void *param_value,
                                   size_t *param_value_size_ret);

    cl_mem clCreatePipe(cl_context context,
                        cl_mem_flags flags,
                        cl_uint pipe_packet_size,
                        cl_uint pipe_max_packets,
                        const cl_pipe_properties *properties,
                        cl_int *errcode_ret);

    void *clSVMAlloc(cl_context context,
                     cl_svm_mem_flags flags,
                     size_t size,
                     unsigned int alignment);
    void clSVMFree(cl_context context,
                   void *svm_pointer);
    cl_int clEnqueueSVMMap(cl_command_queue command_queue,
                           cl_bool blocking_map,
                           cl_map_flags map_flags,
                           void *svm_ptr,
                           size_t size,
                           cl_uint num_events_in_wait_list,
                           const cl_event *event_wait_list,
                           cl_event *event);
    cl_int clEnqueueSVMUnmap(cl_command_queue command_queue,
                             void *svm_ptr,
                             cl_uint  num_events_in_wait_list,
                             const cl_event *event_wait_list,
                             cl_event *event);
    cl_int clSetKernelArgSVMPointer(cl_kernel kernel,
                                    cl_uint arg_index,
                                    const void *arg_value);
    cl_int clEnqueueSVMMemcpy(cl_command_queue command_queue,
                              cl_bool blocking_copy,
                              void *dst_ptr,
                              const void *src_ptr,
                              size_t size,
                              cl_uint num_events_in_wait_list,
                              const cl_event *event_wait_list,
                              cl_event *event);
    cl_int clEnqueueSVMMemFill(cl_command_queue command_queue,
                               void *svm_ptr,
                               const void *pattern,
                               size_t pattern_size,
                               size_t size,
                               cl_uint num_events_in_wait_list,
                               const cl_event *event_wait_list,
                               cl_event *event);

    cl_event clCreateUserEvent (cl_context context,
 	                            cl_int *errcode_ret);

 	cl_int clSetUserEventStatus (cl_event event,
 	                             cl_int execution_status);

 	cl_int clGetEventInfo(cl_event event,
 	                      cl_event_info param_name,
 	                      size_t param_value_size,
 	                      void *param_value,
 	                      size_t *param_value_size_ret);

    cl_int clRetainEvent(cl_event event);

    cl_int clSetEventCallback(cl_event event,
 	                          cl_int command_exec_callback_type,
 	                          void *pfn_event_notify,
 	                          void *user_data);

 	cl_int clGetCommandQueueInfo   (cl_command_queue command_queue,
 	                                cl_command_queue_info param_name,
 	                                size_t  param_value_size ,
 	                                void  *param_value ,
 	                                size_t  *param_value_size_ret );
