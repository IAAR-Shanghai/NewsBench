<!-- Navbar.vue -->
<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <a class="navbar-brand" href="#">
    <img src="../assets//logo.png" width="30" height="30" class="d-inline-block align-top" alt="">
    News Benchmark
  </a>

  <div class="collapse navbar-collapse justify-content-end" id="navbarNav" style="text-align: right; margin-right: 20px;">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link active" href="#" style="text-align: left;">Home</a>
      </li>
      <li class="nav-item">
        <a class="nav-link active" href="#">Paper</a>
      </li>
      <li class="nav-item">
        <a class="nav-link active" href="#">Code</a>
      </li>
      <li class="nav-item">
        <a class="nav-link active" href="/leaderboard">Leaderboard</a>
      </li>
      <!-- <li class="nav-item">
        <a class="nav-link active">FAQ</a>
      </li>
      <li class="nav-item">
        <a class="nav-link active">About</a>
      </li> -->
    </ul>
  </div>
</nav>


</template>

<script>
export default {
  name: 'MyNavbar'
}
</script>

<style>
/* .navbarNav {
  text-align: right;
} */


</style>
