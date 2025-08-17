"""
Simple data structure for inputs and outputs
"""

from dataclasses import dataclass
from typing import List


@dataclass
class InputOutput:
    """Simple input-output pair"""
    input: str
    output: List[str]

# Your examples
EXAMPLES = [
    InputOutput(
        input="""
            The concept of sustainability was originally coined in forestry, where it means never harvesting
            more than what the forest yields in new growth [2]. The word Nachhaltigkeit (the German term for
            sustainability) was first used with this meaning in 1713 [3]. The concern with preserving natural
            resources for the future is perennial, of course: undoubtedly our Palaeolithic ancestors worried about
            their prey becoming extinct, and early farmers must have been apprehensive about maintaining soil
            fertility. Traditional beliefs enjoined thinking in terms of stewardship and concern for future
            generations, as expressed in the oft-quoted words of a Nigerian tribal chief who saw the community as
            consisting of “many dead, few living and countless others unborn” [4,5]. Perhaps there have always
            been two opposing views of the relation between humankind and nature: one which stresses adaptation
            and harmony, and another which sees nature as something to be conquered. While this latter view may
            have been rather dominant in Western civilization at least in recent centuries, its counterpoint has
            never been absent.
            Sustainability (without necessarily using the word) is a natural topic of study for economists: after
            all, the scarcity of resources is of central concern to the dismal science. A famous example is the work
            of Thomas Malthus, who published his theory about looming mass starvation (due to the inability of
            available agricultural land to feed an expanding population) in 1798. A theory on the optimal rate of
            exploitation of non-renewable resource which is still relevant today was formulated by Harold
            Hotelling, an American economist, in 1931 [6]. We shall have more to say about his views later.
            A milestone in capturing the attention of global public policy was the report of the Club of
            Rome [7], which predicted that many natural resources crucial to our survival would be exhausted
            within one or two generations. Such pessimism is unbecoming in public policy which is, after all,
            supposed to be about improving things. Therefore, the report of the UN World Commission on
            Environment and Development, better known as the Brundtland Report after its chairperson, was
            welcomed for showing a way out of impending doom. It was this report which adopted the concept of
            sustainability and gave it the widespread recognition it enjoys today.
            The question which Brundtland and her colleagues posed themselves was: how can the aspirations
            of the world’s nations for a better life be reconciled with limited natural resources and the dangers of
            environmental degradation? Their answer is sustainable development, in the Commission’s words:
            development that meets the needs of the present without compromising the ability of future
            generations to meet their own needs [1].
            Thus, environmental concerns are important, but the basic argument is one of welfare, seen in a
            context of inter-generational equity. We should care for the environment not because of its intrinsic
            value, but in order to preserve resources for our children.
            Since that time, there have been two major developments in the concept of sustainability: one, its
            interpretation in terms of three dimensions, which must be in harmony: social, economic and
            environmental. Two, the distinction between ‘strong’ and ‘weak’ sustainability. These two
            developments are discussed critically in the Sections 3–4 and 5–6, respectively.
        """,
        output=[
        """
            The concept of sustainability was originally coined in forestry,
            where it means never harvesting more than what the forest yields in new growth [2].
            The word Nachhaltigkeit (the German term for sustainability)
            was first used with this meaning in 1713 [3].
            The concern with preserving natural resources for the future is perennial,
            of course: undoubtedly our Palaeolithic ancestors worried about their prey
            becoming extinct, and early farmers must have been apprehensive about maintaining soil
            fertility. Traditional beliefs enjoined thinking in terms of stewardship and concern
            for future generations, as expressed in the oft-quoted words of a Nigerian tribal
            chief who saw the community as consisting of “many dead, few living and countless
            others unborn” [4,5]. Perhaps there have always been two opposing views of the relation
            between humankind and nature: one which stresses adaptation and harmony, and another
            which sees nature as something to be conquered. While this latter view may have been
            rather dominant in Western civilization at least in recent centuries, its counterpoint
            has never been absent.
        """,
        """
            Sustainability (without necessarily using the word) is a natural topic of study for economists:
            after all, the scarcity of resources is of central concern to the dismal science.
            A famous example is the work of Thomas Malthus, who published his theory about looming mass starvation
            (due to the inability of available agricultural land to feed an expanding population) in 1798.
            A theory on the optimal rate of exploitation of non-renewable resources which is still relevant today was
            formulated by Harold Hotelling, an American economist, in 1931 [6]. We shall have more to say about his views later.
            A milestone in capturing the attention of global public policy was the report of the Club of Rome [7],
            which predicted that many natural resources crucial to our survival would be exhausted within one or two generations.
            Such pessimism is unbecoming in public policy which is, after all, supposed to be about improving things.
            Therefore, the report of the UN World Commission on Environment and Development, better known as the Brundtland
            Report after its chairperson, was welcomed for showing a way out of impending doom. It was this report which adopted
            the concept of sustainability and gave it the widespread recognition it enjoys today.
        """,
        """
            The question which Brundtland and her colleagues posed themselves was: how can the aspirations of the world’s
            nations for a better life be reconciled with limited natural resources and the dangers of environmental degradation?
            Their answer is sustainable development, in the Commission’s words: development that meets the needs of the present without
            compromising the ability of future generations to meet their own needs [1]. Thus, environmental concerns are important,
            but the basic argument is one of welfare, seen in a context of inter-generational equity. We should care for the environment
            not because of its intrinsic value, but in order to preserve resources for our children. Since that time, there have been two
            major developments in the concept of sustainability: one, its interpretation in terms of three dimensions, which must be in
            harmony—social, economic and environmental. Two, the distinction between ‘strong’ and ‘weak’ sustainability.
            These two developments are discussed critically in the Sections 3–4 and 5–6, respectively.
         """
         ]
    ),

    # Add more examples here
    InputOutput(
        input="""
            The Brundtland report speaks of two concerns that should be reconciled: development and the
            environment. They can also be interpreted as needs versus resources, or as the short versus the long
            term. Today, however, sustainability is almost always seen in terms of three dimensions: social,
            economic and environmental [8-11]. This is embodied in the definition of sustainability adopted by the
            United Nations in its Agenda for Development:
            Development is a multidimensional undertaking to achieve a higher quality of life for all
            people. Economic development, social development and environmental protection are
            interdependent and mutually reinforcing components of sustainable development [12].
            But what are economic and social development and how are they different? Robert Gibson, a
            political scientist, says that the distinction is needed because “material gains are not sufficient measures
            or preservers of human well-being” [13]. The same author also suggests that the three dimensions or
            ‘pillars’ reflect the disciplines of those who study sustainability, adding for good measure that a
            cultural and a political pillar could also be included [13]. Gibson himself, by the way, rejects the idea
            of pillars altogether and instead formulates seven principles on which sustainability could be based.
            The idea of sustainability having three dimensions stems from the Triple Bottom Line concept,
            coined by Elkington [14]. As the term bottom line suggests, it originates from the world of
            management science, and Elkington intended it as a way to operationalize corporate social
            responsibility. To the conventional bottom line (profit) should be added care for the environment (the
            planet) as well as being good to people, for instance by providing facilities for the handicapped and
            hiring minorities (the social dimension).
            The goals of business, however, are very different from those of public policy. Although, as in
            business, revenue is needed to cover government expenditure, maximizing the excess of revenue over
            expenditure is not normally considered an appropriate goal for government policy. Government is not
            supposed to be a profit-making venture. The ‘profit’ pillar is therefore translated as the money made by
            the entire country, expressed as gross domestic product (GDP). This then is the economic dimension,
            and the social dimension (‘people’) is everything else connected with human aspirations: equity
            (translated as income distribution), inclusion (commonly operationalized as employment) and health
            (expressed by an indicator such as life expectancy or access to medical services). However, the
            equation of ‘economic’ with money is a very limited view of economics. Moreover, the view is further
            restricted if we confine ourselves to the aggregate amount, and not with its distribution or with what
            the money can buy.
            GDP is intended as a measure of welfare, and as such it is a very useful but also a very incomplete
            and biased one. It is useful for measuring the amount of economic activity and because there are
            relatively good data for it; but it needs to complemented by other indices, such as the Human
            Development Index. These are subjects of study for both economics and sociology, and there is no
            good reason to call one aspect economic and the others social. The sociologist would ask what welfare
            is and how it can be measured (an issue discussed in the next section), whereas the economist’s task
            would be to assess, given human aspirations and the scarcity of resources, what course of action is
            likely to produce the highest degree of satisfaction of those aspirations.
            If there is good reason from a conceptual point of view to prefer a single socio-economic dimension,
            what of its usefulness to policy analysts? Let us consider a hypothetical project which scores very well
            on the environmental dimension but rather poorly on both the social and the economic one. This might
            easily lead a policy-maker to conclude that the project is, on the whole, not a good idea. A
            two-dimensional approach might bring about the opposite judgment: its environmental benefits come
            at a cost in terms of welfare. The environmental dimension may thus receive less weight in a
            three-dimensional approach. Indeed, some authors explicitly state that the three dimensions should
            receive equal weight [15]. Since socio-economic aspects are mostly about the well-being of the present
            generation and environmental ones are about caring for the future, this means the former become twice
            as important as the latter—which violates the Brundtland requirement that development should not
            take place at the expense of future generations.
            Worse, perhaps, is that the contradiction between our desire for a better life and our concern for
            what this may do to the environment is obscured by conceptualizing these two concerns into three
            dimensions, and then suggesting that a solution is possible where all three are in harmony.
            Sustainability then becomes a concept that is equivalent to ‘good’ and thus devoid of any specific
            meaning—a blanket concept to assure stakeholders of the policy’s good intentions. The strength and
            relevance of the original Brundtland concept was precisely that it posed the question of how to
            reconcile one goal ‘development’ with another ‘sustainability’. The two goals are often in tension.
            Therefore, we propose to use the word sustainability in the sense as it was intended by the
            Brundtland Commission, and not as it has been coined later by corporate types and policy-makers. In
            the words of Robert Solow [16]:
            If ‘sustainability’ is anything more than a slogan or expression of emotion, it must amount
            to an injunction to preserve productive capacity for the indefinite future.
            Such a concept must be confronted with the socio-economic dimension of human aspirations for a
            better life: welfare, well-being, development or some similar concept. Which of these concepts it
            should be is the topic of the following section, before returning to our exploration of sustainability.
        """,
    output=[
        """
            The Brundtland report speaks of two concerns that should be reconciled: development and the environment.
            They can also be interpreted as needs versus resources, or as the short versus the long term.
            Today, however, sustainability is almost always seen in terms of three dimensions: social, economic and environmental [8–11].
            This is embodied in the definition of sustainability adopted by the United Nations in its Agenda for Development:
            Development is a multidimensional undertaking to achieve a higher quality of life for all people.
            Economic development, social development and environmental protection are interdependent and mutually reinforcing components of sustainable development [12].
            But what are economic and social development and how are they different? Robert Gibson, a political scientist, says that the distinction is needed because
            “material gains are not sufficient measures or preservers of human well-being” [13].
            The same author also suggests that the three dimensions or ‘pillars’ reflect the disciplines of those who study sustainability,
            adding for good measure that a cultural and a political pillar could also be included [13].
            Gibson himself, by the way, rejects the idea of pillars altogether and instead formulates seven principles on which sustainability could be based.
        """,

        """
            The idea of sustainability having three dimensions stems from the Triple Bottom Line concept, coined by Elkington [14].
            As the term bottom line suggests, it originates from the world of management science, and Elkington intended it as a way to operationalize corporate social responsibility.
            To the conventional bottom line (profit) should be added care for the environment (the planet) as well as being good to people,
            for instance by providing facilities for the handicapped and hiring minorities (the social dimension).
            The goals of business, however, are very different from those of public policy. Although, as in business,
            revenue is needed to cover government expenditure, maximizing the excess of revenue over expenditure is not normally considered
            an appropriate goal for government policy. Government is not supposed to be a profit-making venture.
            The ‘profit’ pillar is therefore translated as the money made by the entire country, expressed as gross domestic product (GDP).
            This then is the economic dimension, and the social dimension (‘people’) is everything else connected with human aspirations:
            equity (translated as income distribution), inclusion (commonly operationalized as employment) and health
            (expressed by an indicator such as life expectancy or access to medical services).
        """,
        """
            However, the equation of ‘economic’ with money is a very limited view of economics. Moreover,
            the view is further restricted if we confine ourselves to the aggregate amount, and not with its distribution or with what the money can buy.
            GDP is intended as a measure of welfare, and as such it is a very useful but also a very incomplete and biased one.
            It is useful for measuring the amount of economic activity and because there are relatively good data for it;
            but it needs to be complemented by other indices, such as the Human Development Index. These are subjects of study for both economics and sociology,
            and there is no good reason to call one aspect economic and the others social.
            The sociologist would ask what welfare is and how it can be measured (an issue discussed in the next section),
            whereas the economist’s task would be to assess, given human aspirations and the scarcity of resources,
            what course of action is likely to produce the highest degree of satisfaction of those aspirations.
            If there is good reason from a conceptual point of view to prefer a single socio-economic dimension, what of its usefulness to policy analysts?
        """,
        """
            Let us consider a hypothetical project which scores very well on the environmental dimension but rather poorly on both the social and the economic one.
            This might easily lead a policy-maker to conclude that the project is, on the whole, not a good idea. 
            A two-dimensional approach might bring about the opposite judgment: its environmental benefits come at a cost in terms of welfare. 
            The environmental dimension may thus receive less weight in a three-dimensional approach. 
            Indeed, some authors explicitly state that the three dimensions should receive equal weight [15].
            Since socio-economic aspects are mostly about the well-being of the present generation and environmental ones are about caring for the future,
            this means the former become twice as important as the latter—which violates the Brundtland requirement that development should not take place
            at the expense of future generations. Worse, perhaps, is that the contradiction between our desire for a better life and our concern 
            for what this may do to the environment is obscured by conceptualizing these two concerns into three dimensions, and then suggesting that
            a solution is possible where all three are in harmony.
        """
        """
            Sustainability then becomes a concept that is equivalent to ‘good’ and thus devoid of any specific meaning—a blanket concept to assure
            stakeholders of the policy’s good intentions. The strength and relevance of the original Brundtland concept was precisely
            that it posed the question of how to reconcile one goal ‘development’ with another ‘sustainability’.
            The two goals are often in tension. Therefore, we propose to use the word sustainability in the sense as it was intended by the Brundtland Commission,
            and not as it has been coined later by corporate types and policy-makers. In the words of Robert Solow [16]:
            If ‘sustainability’ is anything more than a slogan or expression of emotion, it must amount to an injunction to preserve productive capacity for the indefinite future.
            Such a concept must be confronted with the socio-economic dimension of human aspirations for a better life: welfare, well-being,
            development or some similar concept. Which of these concepts it should be is the topic of the following section, before returning to our exploration of sustainability.
        """
            ]
    ),
]
import re

# def strip_text(text):
#     return re.sub(r'\s+', ' ', text.strip())

# Simple access
def get_example(index: int) -> InputOutput:
    """Get example by index"""
    return EXAMPLES[index]

def get_all_inputs() -> List[str]:
    """Get all input texts"""
    return [example.input for example in EXAMPLES]

def get_all_outputs() -> List[List[str]]:
    """Get all output segments"""
    return [example.output for example in EXAMPLES]

def get_all_examples() -> List[InputOutput]:
    return [EXAMPLES[i] for i in range(len(EXAMPLES)) ]

# Usage
if __name__ == "__main__":
    # Get first example
    example = get_example(0)
    print(f"Input: {example.input[:100]}...")
    print(f"Output segments: {len(example.output)}")
    
    