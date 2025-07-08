def stream_output(step_stream):
    for step in step_stream:
        print(step.pretty_output) 