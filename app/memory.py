from dataclasses import dataclass, field


@dataclass
class MemoryStore:
    runs: list[dict] = field(default_factory=list)

    def add(self, run: dict) -> None:
        self.runs.append(run)

    def recent_for_machine(self, machine_id: str, limit: int = 5) -> list[dict]:
        matches = [run for run in self.runs if run.get("machine_id") == machine_id]
        return matches[-limit:]
