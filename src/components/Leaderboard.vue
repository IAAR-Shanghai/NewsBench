<!-- Navbar.vue -->
<template>
  
  <h3 class="text-center">
    Leaderboard
  </h3>

  <div class="table-container">
    <table class="table custom-table">
      <thead class="thead-dark">
        <tr>
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
          <th scope="row">1</th>
          <td>GPT-4-1106</td>
          <td>-</td>
          <td>×</td>
          <td>2.4438</td>
          <td>0.4560</td>
          <td>0.9000</td>
          <td>0.9068</td>
        </tr>
      </tbody>
    </table>
  </div>


</template>

<script>
export default {
  name: 'MyLeaderboard'
}
</script>

<style>
.table-container {
  width: 70%; /* 表格容器占据页面宽度的70% */
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
  font-size: 14px; /* 设置字体大小为14像素 */
}
</style>
