MLS_API_URL = {
    "dev": "https://ab-onprem.dev.sktmls.com",
    "stg": "https://ab-onprem.stg.sktmls.com",
    "prd": "https://ab-onprem.sktmls.com",
}

HDFS_OPTIONS = """-Dfs.s3a.proxy.host=awsproxy.datalake.net \
                 -Dfs.s3a.proxy.port=3128 \
                 -Dfs.s3a.endpoint=s3.ap-northeast-2.amazonaws.com \
                 -Dfs.s3a.security.credential.provider.path=jceks:///user/tairflow/s3_mls.jceks \
                 -Dfs.s3a.fast.upload=true -Dfs.s3a.acl.default=BucketOwnerFullControl"""
