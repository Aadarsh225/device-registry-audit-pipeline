use("device_registry_db");

// db.master_device_audit.find()

// db.master_device_audit.findOne()

// db.master_device_audit.find({scheme:"fonepay"})

// finding the no of transaction based on the scheme
// db.master_device_audit.aggregate([
//     {
//         $group:{
//             _id:"$scheme",
//             total_transaction:{$sum:1}
//         }
//     }
// ])

// finding the total amount of transaction based on the scheme
// db.master_device_audit.aggregate([
//     {
//         $group:{
//             _id:"$scheme",
//             total_amount:{$sum:"$amount"}
//         }
//     }
// ])

// finding total number of transaction based on the status
// db.master_device_audit.aggregate([
//     {
//         $group:{
//             _id:"$status",
//             total_transaction:{$sum:1}
//         }
//     }
// ])

// findinf amount spend based on the status
// db.master_device_audit.aggregate([
//     {
//         $group:{
//             _id:"$status",
//             total_amount:{$sum:"$amount"}
//         }
//     }
// ])

// calculating total no of transaction based on the prefix
// db.master_device_audit.aggregate([
//     {
//         $group:{
//             _id:"$prefix",
//             total_transaction:{$sum:1}
//         }
//     }
// ])

// calculating total amount based on the prefix
// db.master_device_audit.aggregate([
//     {
//         $group:{
//             _id:"$prefix",
//             totalamount:{$sum:"$amount"}
//         }
//     }
// ])

// db.master_device_audit.find({
//   created_at_audit: null
// })

// db.master_device_audit.find({
//   status: null
// })

// db.master_device_audit.find({
//   owner: null
// })

// db.master_device_audit.find({
//     gpay:null
// })

// db.master_device_audit.find({
//     model:null
// })

// checking transaction amount less than 0 
// db.master_device_audit.find({
//   amount: { $lt: 0 }
// })

// Findinf the duplicate machine identifier
// db.master_device_audit.aggregate([
//   {
//     $group: {
//       _id: "$machine_identifier",
//       count: { $sum: 1 }
//     }
//   },
//   {
//     $match: {
//       count: { $gt: 1 }
//     }
//   }
// ])

// finding the device with same serail number
// db.master_device_audit.aggregate([
//     {
//         $group:{
//             _id:"$serial_number",
//             count: {$sum:1}
//         }
//     },
//     {
//         $match:{
//             count:{ $gt:1}
//         }
//     }
// ])

// finding total no of transaction based on the type of the transaction
// db.master_device_audit.aggregate([
//     {
//         $group:{
//             _id:"$type",
//             totaltransaction:{$sum:1}
//         }
//     }
// ])

// finding total amount based on the type of the transaction
// db.master_device_audit.aggregate([
//     {
//          $group:{
//            _id:  "$type",
//             totalamount:{$sum:"$amount"}
//          }
//     }
// ])

// // // finding inside object
// // db.master_device_audit.find({
// //   "gpay.merchantId": "GP001"
// })

// db.master_device_audit.find({
//   "device.service_type": "INVALID"
// })

// db.master_device_audit.find({
//   "gpay.terminalId": null
// })

// db.master_device_audit.find({
//   "phonepe.merchantId": { $exists: true }
// })

// db.master_device_audit.updateMany(
//   { "device.service_type": "INVALID" },
//   {
//     $set: {
//       "device.service_type": "NOTIFY"
//     }
//   }
// )


// Grouping on the basis on device object serveice_type
// db.master_device_audit.aggregate([
//   {
//     $group:{
//       _id:"$device.service_type",
//       total:{$sum:1}
//     }
//   }
// ])

// db.master_device_audit.find(
//   {},
//   {
//     "gpay.merchantId":1,
//     "phonepe.merchantId":1,
//     _id:0
//   }
// )

// total no of transaction based on the basis of the owner
// db.master_device_audit.aggregate([
//   {
//     $group:{
//       _id:"$owner",
//       total_transaction:{$sum:1}
//     }
//   }
// ])


// total amount of transaction done by the owner of the bank
// db.master_device_audit.aggregate([
//     {
//         $group:{
//             _id:"owner",
//             totalamount:{$sum:"$amount"}
//         }
//     }
// ])

// device with null payemne method
db.master_device_audit.find({
  gpay:null,
  phonepe:null,
  paytm:null,
  bhim:null
})
