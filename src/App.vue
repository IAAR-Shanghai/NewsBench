<template>
  <div id="app">
    <!-- <nav class="navbar navbar-expand-lg navbar-dark bg-dark" style="position: fixed; top: 0; left: 0; right: 0;">
      <router-link class="navbar-brand title" to="/">
        News Benchmark
      </router-link>

      <div class="collapse navbar-collapse justify-content-end" id="navbarNav" style="text-align: right; margin-right: 20px;">
        <ul class="navbar-nav">
          <li class="nav-item active">
            <router-link class="nav-link active" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link active" href="https://www.iaar.ac.cn/">Paper</a>
          </li>
          <li class="nav-item">
            <a class="nav-link active" href="https://www.iaar.ac.cn/">Code</a>
          </li>
          <li class="nav-item">
            <router-link class="nav-link active" to="/leaderboard">Leaderboard</router-link>
          </li>
        </ul>
      </div>
    </nav> -->

    <br/>

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
.title {
  margin-left: 50px;
}
</style>
