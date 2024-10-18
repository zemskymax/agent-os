import json
import re
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

MODEL = "Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4"
# MODEL = "Qwen/Qwen2.5-7B-Instruct"
NUM_GPUs = 1

class VllmWrapper:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL)

        self.sampling_params = SamplingParams(temperature=0.2, top_k=100, top_p=0.5, repetition_penalty=1.05, max_tokens=1000)

        self.llm = LLM(model=MODEL, gpu_memory_utilization=0.9, max_model_len=1000, tensor_parallel_size=NUM_GPUs, seed=17, quantization="GPTQ", enforce_eager=False)

    def _try_parse_tool_calls(self, content: str):
        """Try parse the tool calls.
            {'role': 'assistant', 'content': '', 'tool_calls': [{'function': {'name': 'WeatherFromLatLongTool', 'arguments': {'latitude': 31.7788242, 'longitude': 35.2257626}}}]}
        """
        tool_calls = []
        offset = 0
        for i, m in enumerate(re.finditer(r"<tool_call>\n(.+)?\n</tool_call>", content)):
            if i == 0:
                offset = m.start()
            try:
                func = json.loads(m.group(1))
                tool_calls.append({"type": "function", "function": func})
                if isinstance(func["arguments"], str):
                    func["arguments"] = json.loads(func["arguments"])
            except json.JSONDecodeError as e:
                print(f"Failed to parse tool calls: the content is {m.group(1)} and {e}")
                pass
        if tool_calls:
            if offset > 0 and content[:offset].strip():
                c = content[:offset]
            else: 
                c = ""
            return {"role": "assistant", "content": c, "tool_calls": tool_calls}
        return {"role": "assistant", "content": re.sub(r"<\|im_end\|>$", "", content)}

    def generate_response(self, messages, tools):
        text = self.tokenizer.apply_chat_template(
            messages,
            tools=tools,
            tokenize=False,
            add_generation_prompt=True,
            return_tensors="pt"
        )
        # text = self.tokenizer.apply_chat_template(messages, tools=tools, add_generation_prompt=True, return_dict=True, return_tensors="pt")
        response = self.llm.generate([text], self.sampling_params)

        for output in response:
            try:
                js = self._try_parse_tool_calls(output.outputs[0].text.strip())
            except Exception as ex:
                print(f"Exception (while generating the response): {ex}!")
                continue

            # print(f"--> output as JSON:\n {js})")
            return js
        return ""
