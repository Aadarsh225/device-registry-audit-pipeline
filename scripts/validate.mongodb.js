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
db.master_device_audit.aggregate([
    {
        $group:{
            _id:"$prefix",
            totalamount:{$sum:"$amount"}
        }
    }
])