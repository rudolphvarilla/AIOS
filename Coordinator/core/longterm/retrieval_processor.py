from core.longterm.context import LongTermContext
from core.longterm.context import RetrievedMemory


class LongTermRetrievalProcessor:

    def process(

        self,

        query,

        memories,

        perception=None,

        context=None,

    ):

        result = LongTermContext()

        for memory in memories:

            reason = self.explain(

                query,

                memory,

            )

            confidence = self.confidence(

                query,

                memory,

            )

            result.retrieved.append(

                RetrievedMemory(

                    memory=memory,

                    reason=reason,

                    confidence=confidence,

                )

            )

        result.summary = self.build_summary(result)

        return result