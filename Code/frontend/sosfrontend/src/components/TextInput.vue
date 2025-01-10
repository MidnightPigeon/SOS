<template>
  <div>
    <h1>提交长文本数据</h1>
    <!-- 文本输入框 -->
    <textarea v-model="longText" placeholder="请输入长文本"></textarea>
    
    <!-- 提交按钮 -->
    <button @click="submitData">提交</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      longText: '',  // 用来存储用户输入的长文本
    };
  },
  methods: {
    // 提交数据的方法
    async submitData() {
      try {
        // 将长文本转换为 JSON 格式
        const jsonData = this.convertTextToJson(this.longText);

        // 控制台输出 JSON 数据
        console.log(JSON.stringify(jsonData));

        // 使用 axios 将 JSON 数据发送到后端
        const response = await axios.post('https://127.0.0.1:8000/upload-text', jsonData, {
          headers: {
            'Content-Type': 'application/json',
          },
        });

        // 后端返回的响应
        console.log('响应:', response.data);
      } catch (error) {
        console.error('请求失败:', error);
      }
    },

    // 将长文本转换为 JSON 格式
    convertTextToJson(text) {
      // 假设我们只是简单地将长文本放入 JSON 对象中的 "content" 字段
      return {
        "content": text
      };
    }
  }
};
</script>

<style scoped>
/* 可以在此添加样式 */
textarea {
  width: 100%;
  height: 150px;
  margin-bottom: 10px;
}

button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>