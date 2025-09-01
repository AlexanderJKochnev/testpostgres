// init-replica.js
// init-replica.js
print("=== Инициализация Replica Set rs0 ===");

sleep(20000); // ждём mongod

let result;
try {
  result = rs.initiate({
    _id: "rs0",
    members: [
      { _id: 0, host: "mongodb:27017" }
    ]
  });
  printjson(result); // ← Выводим результат
} catch (e) {
  print("❌ Ошибка при инициализации Replica Set:");
  printjson(e);
  exit(1); // ← Контейнер упадёт — видно в `docker-compose ps`
}

// Ждём, пока узел станет PRIMARY
let status;
for (let i = 0; i < 30; i++) {
  sleep(2000);
  try {
    status = rs.status();
    if (status.myState === 1) {
      print("✅ Узел стал PRIMARY");
      exit(0);
    } else if (status.myState === 2) {
      print("🔧 Узел стал SECONDARY");
      exit(0);
    } else {
      print(`🔧 Состояние узла: ${status.myState}, ждём...`);
    }
  } catch (e) {
    print(`⚠️ rs.status() ошибка: ${e}`);
  }
}

print("❌ Не удалось дождаться состояния PRIMARY/SECONDARY");
printjson(status);
exit(1);