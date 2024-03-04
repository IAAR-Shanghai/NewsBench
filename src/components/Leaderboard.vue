<!-- Navbar.vue -->
<template>
  
  <div>

    <br/>

    <h3 class="text-center">
      <img src="../assets/paper.png" width="60" height="60" class="d-inline-block align-center" alt="">
      NewsBench Leaderboard
    </h3>

    <br/>

    <div class="table-container">
      <table class="table table-hover table-borderless">
        <thead class="thead-light">
          <tr class="table-dark">
            <th scope="col">#</th>
            <th scope="col">Model</th>
            <th scope="col">#Parameters</th>
            <th scope="col">Open Weights</th>
            <th scope="col">JWP-Generation</th>
            <th scope="col">JWP-Multiple</th>
            <th scope="col">SA-Generation</th>
            <th scope="col">SA-Multiple</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row">1</th>
            <td>GPT-4-1106</td>
            <td>-</td>
            <td>×</td>
            <td>2.4438</td>
            <td>0.4560</td>
            <td>0.9000</td>
            <td>0.9068</td>
          </tr>
          <tr>
            <th scope="row">2</th>
            <td>GPT-3.5-turbo</td>
            <td>-</td>
            <td>×</td>
            <td>2.3758</td>
            <td>0.3070</td>
            <td>0.7892</td>
            <td>0.6281</td>
          </tr>
          <tr>
            <th scope="row">3</th>
            <td>ERNIE Bot</td>
            <td>-</td>
            <td>×</td>
            <td>2.4112</td>
            <td>0.5264</td>
            <td>0.8456</td>
            <td>0.8867</td>
          </tr>
          <tr>
            <th scope="row">4</th>
            <td>Baichuan2-13B</td>
            <td>13B</td>
            <td>√</td>
            <td>2.3392</td>
            <td>0.3452</td>
            <td>0.7211</td>
            <td>0.5842</td>
          </tr>
          <tr>
            <th scope="row">5</th>
            <td>Baichuan2-53B</td>
            <td>53B</td>
            <td>√</td>
            <td>2.4088</td>
            <td>0.3456</td>
            <td>0.7883</td>
            <td>0.6628</td>
          </tr>
          <tr>
            <th scope="row">6</th>
            <td>ChatGLM2-6B</td>
            <td>6B</td>
            <td>√</td>
            <td>2.2658</td>
            <td>0.3103</td>
            <td>0.7534</td>
            <td>0.5228</td>
          </tr>
          <tr>
            <th scope="row">7</th>
            <td>ChatGLM3-6B</td>
            <td>6B</td>
            <td>√</td>
            <td>2.3082</td>
            <td>0.3303</td>
            <td>0.7599</td>
            <td>0.4883</td>
          </tr>
          <tr>
            <th scope="row">8</th>
            <td>Aquila-34B</td>
            <td>34B</td>
            <td>√</td>
            <td>2.1808</td>
            <td>0.2401</td>
            <td>0.7885</td>
            <td>0.2687</td>
          </tr>
          <tr>
            <th scope="row">9</th>
            <td>InternLM-20B</td>
            <td>20B</td>
            <td>√</td>
            <td>2.2208</td>
            <td>0.4008</td>
            <td>0.7669</td>
            <td>0.5813</td>
          </tr>
          <tr>
            <th scope="row">10</th>
            <td>Qwen-14B</td>
            <td>14B</td>
            <td>√</td>
            <td>2.3796</td>
            <td>0.4408</td>
            <td>0.7053</td>
            <td>0.7324</td>
          </tr>
          <tr>
            <th scope="row">11</th>
            <td>Xinyu2-70B</td>
            <td>70B</td>
            <td>×</td>
            <td>2.2916</td>
            <td>0.3958</td>
            <td>0.7393</td>
            <td>0.5972</td>
          </tr>
          <tr>
            <th scope="row">12</th>
            <td>Xverse</td>
            <td>13B</td>
            <td>√</td>
            <td>2.3968</td>
            <td>0.3861</td>
            <td>0.7702</td>
            <td>0.5948</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>


</template>

<script>
export default {
  name: 'MyLeaderboard'
}
</script>

<style>
.table-container {
  width: 80%; /* 表格容器占据页面宽度的70% */
  margin: 0 auto; /* 居中显示 */
}
.custom-table {
  width: 100%;
  border-collapse: collapse;
}

.custom-table th,
.custom-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
  font-size: 25px; /* 设置字体大小为14像素 */
}
h3 {
    text-align: center;
    margin-top: 50px;
    font-weight: bold;
  }
</style>
