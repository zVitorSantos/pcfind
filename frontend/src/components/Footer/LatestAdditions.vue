<template>
  <div class="latest-additions">
    <h2>Últimas Adições</h2>
    <ul>
      <li>Kabum possui adição de valores automatizada.</li>
      <li>Lista de Subtotais corrigida.</li>
      <li>Cálculo agora considera seleção do usuário.</li>
      <li>Adição manual de produtos.</li>
      <li>...</li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'LatestAdditions',
  // ...
}
</script>

<style scoped>
.latest-additions {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: justify;
}

h2 {
  font-size: 1em;
  margin: 0.2em 0;
  text-align: center;
}

ul {
  padding: 0;
  margin: 0;
}

li {
  font-size: 0.7em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>