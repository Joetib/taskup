<template>
    <footer>
    <p id="copyright">&copy; 2021 TaskUp, KNUST </p>
    <div><a href="https://github.com/Joetib/taskup" target="_blank" ><i class="fab fa-github transition"></i> </a> </div>
    </footer>
</template>



<style scoped>
 footer{
     height: 100px;
     width: 100%;
     background: lightgray;
 }

 #copyright{
     position: relative;
     text-align: center;
     bottom: -70px;
 }

 div{
     position: relative;
      margin: auto;
     font-size: 40px;
     top: -30px;
     width: 50px;
 }

 i:hover,i:active{
     transform: translateY(-5px);
 }
</style>