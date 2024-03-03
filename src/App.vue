<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <a class="navbar-brand" href="/">
        <img src="./assets/logo.png" width="30" height="30" class="d-inline-block align-top" alt="">
        News Benchmark
      </a>

      <div class="collapse navbar-collapse justify-content-end" id="navbarNav" style="text-align: right; margin-right: 20px;">
        <ul class="navbar-nav">
          <li class="nav-item active">
            <a class="nav-link active" href="/" style="text-align: left;">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link active" href="https://www.iaar.ac.cn/">Paper</a>
          </li>
          <li class="nav-item">
            <a class="nav-link active" href="https://www.iaar.ac.cn/">Code</a>
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

    <router-view></router-view>
  </div>
</template>

<script>


export default {
  name: 'App'
}
</script>

<style>
.spacer {
    margin-bottom: 50px; /* 调整所需的间距 */
}
</style>
