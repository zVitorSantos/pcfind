<template>
  <div class="computer-parts">
    <h2>Componentes do Computador</h2>
    <div class="columns">
      <div class="column">
        <h3>Essenciais</h3>
        <ul>
          <li v-for="component in essentialComponents" :key="component">
            {{ component }}
            <span v-if="isInSubtotals(component)" class="checkmark">✔️</span>
          </li>
        </ul>
      </div>
      <div class="column">
        <div class="sub-column">
          <h3>Não Essenciais</h3>
          <ul>
            <li v-for="component in nonEssentialComponents" :key="component">
              {{ component }}
              <span v-if="isInSubtotals(component)" class="checkmark">✔️</span>
            </li>
          </ul>
        </div>
        <div class="sub-column">
          <h3>Periféricos</h3>
          <ul>
            <li v-for="component in peripherals" :key="component">
              {{ component }}
              <span v-if="isInSubtotals(component)" class="checkmark">✔️</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ComputerParts',
  props: ['subtotals'],
  data() {
    return {
      essentialComponents: ['Placa Mãe', 'Processador', 'Memória RAM', 'HD/SSD', 'Placa de Vídeo', 'Fonte de Alimentação', 'Cooler', 'Gabinete'],
      nonEssentialComponents: ['Placa de Rede', 'Placa de Som'],
      peripherals: ['Monitor', 'Teclado', 'Mouse', 'Headset']
    }
  },
  methods: {
    isInSubtotals(component) {
      return this.subtotals && this.subtotals.some(item => item.component === component);
    }
  }
}
</script>

<style scoped>
.computer-parts {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.columns {
  display: flex;
  justify-content: space-around;
  width: 100%;
}

.column {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 50%;
  /* Adjust this value as needed */
  text-align: center;
}

.sub-column {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.checkmark {
  color: green;
}

h2 {
  font-size: 1em;
  margin: 0.2em 0;
  text-align: center;
}

h3 {
  font-size: 0.8em;
  margin-bottom: 0;
  margin-top: 0;
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