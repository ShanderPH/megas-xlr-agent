from dataclasses import dataclass, replace
from decimal import Decimal


class BudgetExceededError(RuntimeError):
    pass


@dataclass(frozen=True)
class Budget:
    soft_limit: Decimal
    hard_limit: Decimal
    consumed: Decimal = Decimal("0")

    def charge(self, amount: Decimal) -> Budget:
        consumed = self.consumed + amount
        if consumed > self.hard_limit:
            raise BudgetExceededError("hard budget exceeded")
        return replace(self, consumed=consumed)
