public ArchivoCharango(String filepath) throws IOException {
    this.path = Paths.get(filepath);
    this.gson = new GsonBuilder().setPrettyPrinting().create();
    this.listType = new TypeToken<List<Charango>>() {}.getType();

    // Si no existe el archivo, crear uno con una lista vacía
    if (!Files.exists(this.path)) {
        Files.createDirectories(this.path.getParent() == null ? Paths.get("") : this.path.getParent());
        try (Writer w = Files.newBufferedWriter(this.path, StandardCharsets.UTF_8)) {
            gson.toJson(new ArrayList<Charango>(), listType, w);
        }
    }
}

// Lee y devuelve todos los Charango del archivo; si el JSON está vacío o corrupto devuelve lista vacía
public synchronized List<Charango> leerTodo() throws IOException {
    try (Reader r = Files.newBufferedReader(this.path, StandardCharsets.UTF_8)) {
        List<Charango> list = gson.fromJson(r, listType);
        return list == null ? new ArrayList<>() : list;
    } catch (JsonSyntaxException e) {
        // JSON inválido -> devolver lista vacía (alternativamente lanzar excepción)
        return new ArrayList<>();
    }
}

// Sobrescribe el archivo con la lista provista
public synchronized void escribirTodos(List<Charango> lista) throws IOException {
    try (Writer w = Files.newBufferedWriter(this.path, StandardCharsets.UTF_8)) {
        gson.toJson(lista, listType, w);
    }
}

// Agrega un Charango al archivo
public synchronized void agregarCharango(Charango c) throws IOException {
    List<Charango> datos = leerTodo();
    datos.add(c);
    escribirTodos(datos);
}

// Elimina charangos cuyo material coincida (ejemplo de borrado por criterio)
public synchronized boolean borrarPorMaterial(String material) throws IOException {
    List<Charango> datos = leerTodo();
    int originalSize = datos.size();
    Iterator<Charango> it = datos.iterator();
    while (it.hasNext()) {
        Charango ch = it.next();
        if (material == null) {
            if (ch.getMaterial() == null) it.remove();
        } else if (material.equals(ch.getMaterial())) {
            it.remove();
        }
    }
    escribirTodos(datos);
    return datos.size() != originalSize;
}

// Vacía el archivo dejando una lista vacía
public synchronized void limpiar() throws IOException {
    escribirTodos(new ArrayList<>());
}

// Devuelve la lista cruda (útil para inspección)
public synchronized List<Charango> listar() throws IOException {
    return leerTodo();
}

// --- Clase POJO Charango incluida para compatibilidad ---
public static class Charango {
    private String material;
    private int nroCuerdas;
    private List<String> cuerdas;

    public Charango() {
        this.material = "madera";
        this.cuerdas = new ArrayList<>();
        this.nroCuerdas = 0;
    }

    public Charango(String material) {
        this.material = material;
        this.cuerdas = new ArrayList<>();
        this.nroCuerdas = 0;
    }

    public String getMaterial() {
        return material;
    }

    public void setMaterial(String material) {
        this.material = material;
    }

    public int getNroCuerdas() {
        return nroCuerdas;
    }

    public void setNroCuerdas(int nroCuerdas) {
        this.nroCuerdas = nroCuerdas;
    }

    public List<String> getCuerdas() {
        return cuerdas;
    }

    public void setCuerdas(List<String> cuerdas) {
        this.cuerdas = cuerdas;
        this.nroCuerdas = cuerdas == null ? 0 : cuerdas.size();
    }
}