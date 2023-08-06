# ProcessEngine mittels Python verwenden

Wenn es darum geht mit Python Prozess zu starten bzw. zu kontrollieren, *External Task* zu verarbeiten 
und Benutzer-Tasks auszuführen, dann ist der `process_engine`-Client richtig. In dieser README 
wird die Verwendung der unterschiedliche Aspekte anhand von Beispielen gezeigt:

- [Vorbereitung der Umgebung](#vorbereitung-der-umgebung)
- [Prozess starten](#prozesss-starten)
- [*External Task* verarbeiten](#external-task-verarbeiten)
- TODO: *User Task* bearbeiten
- TODO: *Event* aus der Prozessengine verarbeiten
- TODO: Verweis auf API-Dokumentation hinzufügen

Die Erweiterung der Client wird dagegen in [CONTRIBUTION.MD](CONTRIBUTION.MD) erklärt.

## Vorbereitung der Umgebung

### Installation des *BPMN-Studio*

Die einfachster Version mit der Interaktion von Python und der ProzessEngine zu starten,
ist die Installation des *BPMN-Studio*, da es die Entwicklung von BPMN-Prozess unterstützt
und eine vorbereitete ProzessEngine mitbringt, die für die ersten Schritte ausreichend ist.

### Prozess erstellen bzw. Beispiel verwenden

Um den ersten Prozess nicht erstellen zu müssen, ist der Prozess *[Hello World](samples/bpmn_models/hello_world.bpmn)* 
vorhanden, dieser muss in das *BPMN-Studio* geladen werden.

![Prozess laden](docs/open_process.png)

### Prozess auf die ProzessEngine veröffentlichen

Um den Prozess verwenden zu können, ist es notwendig, dass
dieser auf doe ProzessEngine veröffentlicht worden ist. Dazu ist es notwendig, den Prozess zu öffenen (1) und anschließend auf die ProzessEngine zu veröffentlichen (2).

![Prozess veröffentlichen](docs/deploy_process.png)

Nachdem der Prozess veröffenticht würde, kann er mittels Python gestartet werden.

![Prozess veröffentlicht](docs/deployed_process.png)

## Prozess starten

Um einen Prozess zu startet ist die Prozess-Id (hier: `hello_world`) und das Start-Event (hier: `the_start_event`) notwendig und die URL (hier: `http://localhost:56000`) unter der die ProzessEngine zu erreichen ist. Nachdem die Informationen bekannt sind, kann der Prozess mit dem entsprechenden angepasseten Script mit Hilfe von Python gestartet werden.

### Beispiel mit nicht blockierendem Client

```python
import logging

from process_engine.process_control import ProcessControlClient

logger = logging.getLogger(__name__)

def main(process_engine_url):
    client = ProcessControlClient(process_engine_url)
    result = client.start_process_instance('hello_world', 'the_start_event')

    logger.info(f"Started process instance with result {result}")

if __name__ == '__main__':
    current_process_engine = 'http://localhost:56000'

    format_template = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    level = logging.DEBUG
    logging.basicConfig(level=level, format=format_template)

    main(current_process_engine)
```

### Beispiel mit blockierendem Client

```python
import logging

from process_engine.process_control import ProcessControlClient, StartCallbackType

logger = logging.getLogger(__name__)

def main(process_engine_url):
    client = ProcessControlClient(process_engine_url)
    result = client.start_process_instance('hello_world', 
        'the_start_event',
        'the_end_event', 
        start_callback=StartCallbackType.ON_ENDEVENT_REACHED
    )

    logger.info(f"Started process instance with result {result}")

if __name__ == '__main__':
    current_process_engine = 'http://localhost:56000'

    format_template = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    level = logging.DEBUG
    logging.basicConfig(level=level, format=format_template)

    main(current_process_engine)
```

## *External Task* verarbeiten

Im Beispiel-Prozess ist bereit eine ServiceTask als *External Task* konfiguriert. 

Für die Verwendung des *External Task* muss ein Topic (hier: `SampleExternalTask`) festgelegt werden und die URL der ProzessEngine (hier: `http://localhost:56000`) bekannt sein.
Nachdem die Informationen bekannt sind, kann der *External Task* mit dem angepassten Script abgearbeitet werden.

Optionen für das Abonnieren von Aufträgen:
- max_tasks: Anzahl der Aufträge (task), die gleichzeitig verarbeitet werden sollen
- long_polling_timeout: Timeout für das Abonnieren
- lock_duration: Wir lange soll der Auftrag reseviert werden, bis er für weitere Worker zur Verfügung steht
- additional_lock_duration: Wir lange soll eine Auftragsreservierung verlängert werden.
- extend_lock_timeout: ...

### Beispiel mit einem Parameter für den Handler *_handler*

```python
import logging

from process_engine.external_task import ExternalTaskClient

logger = logging.getLogger(__name__)

def _handler(payload):
    logger.debug("so some work")
    logger.debug(payload)
    logger.debug("some worker done.")

    return {'some': 'result'}

def main(process_engine_url):
    client = ExternalTaskClient(process_engine_url)

    client.subscribe_to_external_task_for_topic("SampleExternalTask", _handler, max_tasks=5)

    client.start()

if __name__ == '__main__':
    current_process_engine = 'http://localhost:56000'

    format_template = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    level = logging.INFO #logging.DEBUG
    logging.basicConfig(level=level, format=format_template)

    main(current_process_engine)
```

### Beispiel mit einem weiteren Parameter für den Handler *_handler*

```python
import logging

from process_engine.external_task import ExternalTaskClient

logger = logging.getLogger(__name__)

def _handler(payload, task):
    logger.debug("so some work")
    logger.info(f"payload: {payload} for task {task}")
    logger.debug("some worker done.")

    return {'some': 'result'}

def main(process_engine_url):
    client = ExternalTaskClient(process_engine_url)

    client.subscribe_to_external_task_for_topic("SampleExternalTask", _handler)

    client.start()

if __name__ == '__main__':
    current_process_engine = 'http://localhost:56000'

    format_template = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    level = logging.INFO #logging.DEBUG
    logging.basicConfig(level=level, format=format_template)

    main(current_process_engine)
```
