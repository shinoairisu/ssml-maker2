<template>
  <div class="hello">Hello {{ who }} {{ jj() }}</div>
</template>

<script>
module.exports = {
  data: function () {
    return {
      who: "world",
    };
  },
  methods: {
    jj:function(){
      return 15
    }
  }
};
</script>

<style>
.hello {
  background-color: #ffe;
}
</style>