// Generated by gencpp from file elfin_robot_msgs/ElfinIODWriteResponse.msg
// DO NOT EDIT!


#ifndef ELFIN_ROBOT_MSGS_MESSAGE_ELFINIODWRITERESPONSE_H
#define ELFIN_ROBOT_MSGS_MESSAGE_ELFINIODWRITERESPONSE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace elfin_robot_msgs
{
template <class ContainerAllocator>
struct ElfinIODWriteResponse_
{
  typedef ElfinIODWriteResponse_<ContainerAllocator> Type;

  ElfinIODWriteResponse_()
    : success(false)  {
    }
  ElfinIODWriteResponse_(const ContainerAllocator& _alloc)
    : success(false)  {
  (void)_alloc;
    }



   typedef uint8_t _success_type;
  _success_type success;





  typedef boost::shared_ptr< ::elfin_robot_msgs::ElfinIODWriteResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::elfin_robot_msgs::ElfinIODWriteResponse_<ContainerAllocator> const> ConstPtr;

}; // struct ElfinIODWriteResponse_

typedef ::elfin_robot_msgs::ElfinIODWriteResponse_<std::allocator<void> > ElfinIODWriteResponse;

typedef boost::shared_ptr< ::elfin_robot_msgs::ElfinIODWriteResponse > ElfinIODWriteResponsePtr;
typedef boost::shared_ptr< ::elfin_robot_msgs::ElfinIODWriteResponse const> ElfinIODWriteResponseConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::elfin_robot_msgs::ElfinIODWriteResponse_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::elfin_robot_msgs::ElfinIODWriteResponse_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace elfin_robot_msgs

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::elfin_robot_msgs::ElfinIODWriteResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::elfin_robot_msgs::ElfinIODWriteResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::elfin_robot_msgs::ElfinIODWriteResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::elfin_robot_msgs::ElfinIODWriteResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::elfin_robot_msgs::ElfinIODWriteResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::elfin_robot_msgs::ElfinIODWriteResponse_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::elfin_robot_msgs::ElfinIODWriteResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "358e233cde0c8a8bcfea4ce193f8fc15";
  }

  static const char* value(const ::elfin_robot_msgs::ElfinIODWriteResponse_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x358e233cde0c8a8bULL;
  static const uint64_t static_value2 = 0xcfea4ce193f8fc15ULL;
};

template<class ContainerAllocator>
struct DataType< ::elfin_robot_msgs::ElfinIODWriteResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "elfin_robot_msgs/ElfinIODWriteResponse";
  }

  static const char* value(const ::elfin_robot_msgs::ElfinIODWriteResponse_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::elfin_robot_msgs::ElfinIODWriteResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "bool success\n\
\n\
";
  }

  static const char* value(const ::elfin_robot_msgs::ElfinIODWriteResponse_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::elfin_robot_msgs::ElfinIODWriteResponse_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.success);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct ElfinIODWriteResponse_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::elfin_robot_msgs::ElfinIODWriteResponse_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::elfin_robot_msgs::ElfinIODWriteResponse_<ContainerAllocator>& v)
  {
    s << indent << "success: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.success);
  }
};

} // namespace message_operations
} // namespace ros

#endif // ELFIN_ROBOT_MSGS_MESSAGE_ELFINIODWRITERESPONSE_H
