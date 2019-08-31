<?php
include('dbconnect.php');
$qr="update login set status='1' where username='$_GET[id]'";
mysqli_query($con,$qr);
header('location:approveview.php');

?>