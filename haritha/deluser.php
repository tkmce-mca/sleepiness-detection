<?php
include('dbconnect.php');
$qr="delete from login where username='$_GET[id]'";
mysqli_query($con,$qr);
header('location:viewuser.php');

?>