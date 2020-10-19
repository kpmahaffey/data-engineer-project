import etl_program

# To be able to test. If doing the execution from a scheduler, call execute_program with the filename plus location.
if __name__ == "__main__":
    etl_program.execute_program("files/input/movies_metadata.csv")
