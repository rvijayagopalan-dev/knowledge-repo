## ☕ Java 11 Features (LTS Release)

**Java 11** is a Long-Term Support (LTS) release (2018) that introduced important improvements in performance, security, and developer productivity.

---

## 1️⃣ New String Methods

### ✅ `isBlank()`

```java
"   ".isBlank();   // true
```

### ✅ `lines()`

```java
"Hello\nWorld".lines().forEach(System.out::println);
```

### ✅ `strip()`, `stripLeading()`, `stripTrailing()`

Better Unicode support than `trim()`.

```java
"  Hello  ".strip();
```

### ✅ `repeat(int count)`

```java
"Hi ".repeat(3);   // "Hi Hi Hi "
```

---

## 2️⃣ HTTP Client API (Standardized)

New modern HTTP client replacing `HttpURLConnection`.

```java
HttpClient client = HttpClient.newHttpClient();

HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create("https://example.com"))
        .GET()
        .build();

HttpResponse<String> response =
        client.send(request, HttpResponse.BodyHandlers.ofString());

System.out.println(response.body());
```

✔ Supports HTTP/2
✔ WebSocket support
✔ Asynchronous requests

---

## 3️⃣ Local-Variable Syntax for Lambda Parameters

Allows `var` inside lambda parameters.

```java
(var x, var y) -> x + y
```

Useful when using annotations.

---

## 4️⃣ Running Java Without Compilation

Single-file source-code programs can be run directly:

```bash
java HelloWorld.java
```

No need for separate `javac` step.

---

## 5️⃣ New Collection Method: `toArray(IntFunction)`

```java
List<String> list = List.of("A", "B");
String[] array = list.toArray(String[]::new);
```

---

## 6️⃣ Optional Enhancements

New methods:

* `isEmpty()`

```java
Optional<String> opt = Optional.empty();
opt.isEmpty();  // true
```

---

## 7️⃣ Files Utility Methods

### ✅ `readString()`

### ✅ `writeString()`

```java
String content = Files.readString(Path.of("file.txt"));
Files.writeString(Path.of("file.txt"), "Hello");
```

---

## 8️⃣ Nest-Based Access Control

Improves access between nested classes at JVM level.

✔ Removes need for synthetic bridge methods
✔ Better performance

---

## 9️⃣ Flight Recorder (JFR)

Low-overhead production-time profiling tool.

```bash
java -XX:StartFlightRecording filename=recording.jfr
```

Used for:

* Performance analysis
* Debugging production issues

---

## 🔟 Security & Performance Improvements

* TLS 1.3 support
* Removed Java EE & CORBA modules
* Improved garbage collectors
* Better container awareness (Docker)

---

# ❌ Removed Features

* Java EE modules (JAXB, JAX-WS, etc.)
* CORBA
* JavaFX (moved out)

---

# 🎯 Why Java 11 Is Important

* Long-Term Support (LTS)
* Modern HTTP Client
* Production-grade monitoring (JFR)
* Better container (Docker) support
* Cleaner, more compact APIs

---

If you'd like, I can also provide:

* 🔹 Java 11 vs Java 8 comparison
* 🔹 Java 11 interview questions
* 🔹 Migration guide (8 → 11)
* 🔹 Practice programs
* 🔹 Feature comparison table (8 vs 11 vs 17)

Just tell me 🙂
