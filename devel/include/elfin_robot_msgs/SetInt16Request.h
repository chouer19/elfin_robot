// Generated by gencpp from file elfin_robot_msgs/SetInt16Request.msg
// DO NOT EDIT!


#ifndef ELFIN_ROBOT_MSGS_MESSAGE_SETINT16REQUEST_H
#define ELFIN_ROBOT_MSGS_MESSAGE_SETINT16REQUEST_H


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
struct SetInt16Request_
{
  typedef SetInt16Request_<ContainerAllocator> Type;

  SetInt16Request_()
    : data(0)  {
    }
  SetInt16Request_(const ContainerAllocator& _alloc)
    : data(0)  {
  (void)_alloc;
    }



   typedef int16_t _data_type;
  _data_type data;





  typedef boost::shared_ptr< ::elfin_robot_msgs::SetInt16Request_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::elfin_robot_msgs::SetInt16Request_<ContainerAllocator> const> ConstPtr;

}; // struct SetInt16Request_

typedef ::elfin_robot_msgs::SetInt16Request_<std::allocator<void> > SetInt16Request;

typedef boost::shared_ptr< ::elfin_robot_msgs::SetInt16Request > SetInt16RequestPtr;
typedef boost::shared_ptr< ::elfin_robot_msgs::SetInt16Request const> SetInt16RequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::elfin_robot_msgs::SetInt16Request_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::elfin_robot_msgs::SetInt16Request_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace elfin_robot_msgs

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg'], 'elfin_robot_msgs': ['/home/chouer/workspace/rospace/elfin/src/elfin_robot-kinetic-devel/elfin_robot_msgs/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::elfin_robot_msgs::SetInt16Request_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::elfin_robot_msgs::SetInt16Request_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::elfin_robot_msgs::SetInt16Request_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::elfin_robot_msgs::SetInt16Request_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::elfin_robot_msgs::SetInt16Request_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::elfin_robot_msgs::SetInt16Request_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::elfin_robot_msgs::SetInt16Request_<ContainerAllocator> >
{
  static const char* value()
  {
    return "8524586e34fbd7cb1c08c5f5f1ca0e57";
  }

  static const char* value(const ::elfin_robot_msgs::SetInt16Request_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x8524586e34fbd7cbULL;
  static const uint64_t static_value2 = 0x1c08c5f5f1ca0e57ULL;
};

template<class ContainerAllocator>
struct DataType< ::elfin_robot_msgs::SetInt16Request_<ContainerAllocator> >
{
  static const char* value()
  {
    return "elfin_robot_msgs/SetInt16Request";
  }

  static const char* value(const ::elfin_robot_msgs::SetInt16Request_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::elfin_robot_msgs::SetInt16Request_<ContainerAllocator> >
{
  static const char* value()
  {
    return "int16 data\n\
";
  }

  static const char* value(const ::elfin_robot_msgs::SetInt16Request_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::elfin_robot_msgs::SetInt16Request_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.data);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct SetInt16Request_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::elfin_robot_msgs::SetInt16Request_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::elfin_robot_msgs::SetInt16Request_<ContainerAllocator>& v)
  {
    s << indent << "data: ";
    Printer<int16_t>::stream(s, indent + "  ", v.data);
  }
};

} // namespace message_operations
} // namespace ros

#endif // ELFIN_ROBOT_MSGS_MESSAGE_SETINT16REQUEST_H
