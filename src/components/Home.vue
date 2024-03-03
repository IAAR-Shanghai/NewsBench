<!-- Navbar.vue -->
<template>
  
  <h3 class="text-center">
    <a class="navbar-brand" href="#">
    <img src="../assets/logo.png" width="30" height="30" class="d-inline-block align-top" alt=""></a>
    News Benchmark
  </h3>

  <p class="paragraph">This study presents NewsBench, a novel benchmak framework developed to evaluate the capabiity of Large Lanquage Models (lMs)in Chinese jouralisticWriting Proficiency (JWP) and their Safety Adherence (SA), addressing the gap between journalistic ethics and the risks associated with Al utilization. Comprising1.267 tasks across 5 editoral applications, 7 aspects (incuding safety and iouralisic wrting with 4 detaled facets), and spanning 24 news topics domains,NewsBench emplys wo GPT-4 based automalic evalualion proiocols validated by buman assessment 0ur comprehensive anawsis of 41 ulMs highightedGPT-4 and ERNlE Bot as top performers, yet revealed a relative deficiency in joumalisic ethic adherence duing creative wrting tasks. These findings underscorthe need for enhanced ethical quidance in Al-generated joumalisic content, marking a step fonward in aigning Al capablies with jouralistic standards andsafety considerations.</p>

  <footer>
    &copy; 2024 <a href="https://www.iaar.ac.cn/" style="color: black;">IAAR</a> All Rights Reserved.
  </footer>

</template>

<script>
export default {
  name: 'MyHome'
}
</script>

<style>
  h3 {
    text-align: center;
    margin-top: 50px;
    font-weight: bold;
  }

  .paragraph {
    text-align: justify;
    margin-top: 30px; /* 与h3保持一段距离 */
    margin-left: 100px;
    margin-right: 100px;
  }

  footer {
    text-align: center;
    margin-top: 100px;
  }

</style>
