<script src="fetch-institutes.js">
fetch('/api/institutes?country=India&name=technology')
  .then(res => res.json())
  .then(data => console.log("Institutes:", data))
  .catch(err => console.error("Error fetching data:", err));
</script>
