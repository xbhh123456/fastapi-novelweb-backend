<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <button @click="testApiStatus">测试API状态</button>
    <button @click="testGenerateImage">测试图片生成</button>
    <input type="file" @change="handleFileUpload" />
    <button @click="testLineart">测试线稿化</button>
    <p v-if="apiResponse">{{ apiResponse }}</p>
  </div>
</template>

<script>
import { getApiStatus, generateImage, lineart } from '../api';

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data() {
    return {
      apiResponse: null,
      selectedFile: null
    };
  },
  methods: {
    async testApiStatus() {
      try {
        const response = await getApiStatus();
        this.apiResponse = JSON.stringify(response, null, 2);
      } catch (error) {
        this.apiResponse = `Error: ${error.message}`;
      }
    },
    async testGenerateImage() {
      try {
        const data = {
          prompt: 'a beautiful landscape',
          width: 512,
          height: 512
        };
        const response = await generateImage(data);
        this.apiResponse = JSON.stringify(response, null, 2);
      } catch (error) {
        this.apiResponse = `Error: ${error.message}`;
      }
    },
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    async testLineart() {
      if (!this.selectedFile) {
        this.apiResponse = '请先选择一个文件！';
        return;
      }
      try {
        const response = await lineart(this.selectedFile);
        this.apiResponse = JSON.stringify(response, null, 2);
      } catch (error) {
        this.apiResponse = `Error: ${error.message}`;
      }
    }
  }
};
</script>

<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
button {
  margin: 10px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
pre {
  background-color: #f0f0f0;
  padding: 15px;
  border-radius: 5px;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
